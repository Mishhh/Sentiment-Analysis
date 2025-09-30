import pandas as pd
import requests
from lxml import etree
import praw
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
from dotenv import load_dotenv
import os
import praw

# Initialize sentiment analyzer once
analyzer = SentimentIntensityAnalyzer()


# -------------------- SENTIMENT HELPER --------------------
def analyze_sentiment(text):
    """Return sentiment label and compound score."""
    score = analyzer.polarity_scores(text)['compound']
    if score > 0.05:
        sentiment = "Positive"
    elif score < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, round(score, 3)


# -------------------- NEWS SCRAPER --------------------
def fetch_news(query):
    """Fetch news articles from Google News RSS feed."""
    print(f"\nFetching News for: {query}")

    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(url, timeout=10)
    root = etree.fromstring(response.content)

    data = []
    for item in root.findall(".//item"):
        title = item.findtext("title", "No Title")
        link = item.findtext("link", "")
        date = item.findtext("pubDate", "")
        source = item.findtext("source", "Unknown")

        sentiment, score = analyze_sentiment(title)

        data.append({
            "Platform": "News",
            "Title": title,
            "Source": source,
            "Published Date": date,
            "Link": link,
            "Sentiment": sentiment,
            "Compound": score,
            "Keyword": query
        })

    df = pd.DataFrame(data)
    print(f"✅ {len(df)} news articles found.")
    return df


# -------------------- REDDIT SCRAPER --------------------
def fetch_reddit(query):
    """Fetch Reddit posts using PRAW."""
    print(f"\nFetching Reddit data for: {query}")

    load_dotenv()
    reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    posts = []
    for post in reddit.subreddit("all").search(query, limit=50, sort="top"):
        if post.is_self:  # only text-based posts
            text = post.title + " " + post.selftext
            sentiment, score = analyze_sentiment(text)

            posts.append({
                "Platform": "Reddit",
                "Title": post.title,
                "Text": post.selftext[:200],  # short preview
                "Score": post.score,
                "Comments": post.num_comments,
                "Posted Date": datetime.utcfromtimestamp(post.created_utc),
                "Link": post.url,
                "Sentiment": sentiment,
                "Compound": score,
                "Keyword": query
            })

    df = pd.DataFrame(posts)
    print(f"✅ {len(df)} Reddit posts found.")
    return df


# -------------------- COMBINE BOTH --------------------
def get_combined_data(query):
    """Combine News + Reddit data."""
    news_df = fetch_news(query)
    reddit_df = fetch_reddit(query)

    combined_df = pd.concat([news_df, reddit_df], ignore_index=True)
    print(f"\n📊 Total records combined: {len(combined_df)}")

    return combined_df


# -------------------- RUN DIRECTLY --------------------
if __name__ == "__main__":
    query = None
    df = get_combined_data(query)

    if not df.empty:
        print("\nSample data:")
        print(df.head(5))
        df.to_csv(f"{query.lower()}_combined.csv", index=False)
        print(f"\n✅ Saved as {query.lower()}_combined.csv")

