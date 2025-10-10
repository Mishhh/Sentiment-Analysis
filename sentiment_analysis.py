import os
import praw
import pandas as pd
import feedparser
from datetime import datetime
from requests.utils import quote
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# ------------------------
# Setup
# ------------------------
load_dotenv()
analyzer = SentimentIntensityAnalyzer()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# ------------------------
# Sentiment Analysis
# ------------------------
def analyze_sentiment(text):
    """Return sentiment label and compound score."""
    score = analyzer.polarity_scores(text)['compound']
    if score > 0.05:
        sentiment = "Positive"
    elif score < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, abs(round(score * 100, 2))

# ------------------------
# Search Query Generator
# ------------------------
def get_search_queries(entity_type, query):
    entity_type = entity_type.lower()
    query = query.strip()

    queries = {
    "brand": {
        "news": [
            f"{query} news", f"{query} reviews", f"{query} product launch",
            f"{query} update", f"{query} announcement", f"{query} controversy", 
            f"{query} financial results", f"{query} quarterly earnings",
            f"{query} stock performance", f"{query} revenue report", f"{query} market share",
            f"{query} partnership", f"{query} acquisition",f"{query} customer feedback" , f"{query} sustainability",
        ],
        "reddit": [
            f"{query}", f"{query} reviews", f"{query} experience",
            f"{query} issues", f"{query} product feedback", f"{query} performance",
            f"{query} comparison", f"{query} customer service", f"{query} investment", f"{query} controversy",
        ],
    },

    "person": {
        "news": [
            f"{query} news", f"{query} interview", f"{query} statement",
            f"{query} public appearance", f"{query} controversy", f"{query} award",
            f"{query} criticism", f"{query} appreciation", f"{query} achievements", f"{query} opinion piece",
        ],
        "reddit": [
            f"{query}", f"{query} controversy", f"{query} AMA",
            f"{query} opinion", f"{query} discussion", f"{query} fan reactions",
            f"{query} appreciation", f"{query} criticism", f"{query} debate",
        ],
    },

    "topic": {
        "news": [
            f"{query} news", f"{query} latest updates", f"{query} trend", f"{query} analysis",
            f"{query} global impact", f"{query} report", f"{query} public opinion", f"{query} controversy",
            f"{query} expert commentary", f"{query} awareness campaign",
        ],
        "reddit": [
            f"{query}", f"{query} discussion", f"{query} experience",f"{query} opinion",
            f"{query} community debate", f"{query} reactions", f"{query} analysis", f"{query} awareness",
            f"{query} insights",
        ],
    },
}

    return queries.get(entity_type, queries["topic"])

# ------------------------
# Google News Scraper
# ------------------------
def search_news(news_queries, entity_name):

    results = []
    for query in news_queries:
        """Fetch news articles from Google News RSS feed."""
        print(f" Fetching News for: {query}")

        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            sentiment, score = analyze_sentiment(entry.title)
            results.append({
                "Platform": "News",
                "Query": query,
                "Title": entry.title,
                "Published Date": entry.get("published", "Unknown"),
                "Link": entry.link,
                "Sentiment": sentiment,
                "Sentiment Percent": score
            })
    df =  pd.DataFrame(results).drop_duplicates(subset=["Title", "Link"])
    print(f"✅ {len(df)} news articles found.")
    return df

# ------------------------
# Reddit Scraper
# ------------------------
def search_reddit(reddit_queries, entity_name):
   
   results = []
   for query in reddit_queries:
    """Fetch Reddit posts using PRAW."""
    print(f" Fetching Reddit data for: {query}")
   
    for post in reddit.subreddit("all").search(query, sort="relevance", limit=20):
            # Filter: Keep only posts where the query is in the title or selftext
            if entity_name.lower() not in post.title.lower() and query.lower() not in post.selftext.lower():
                continue
            text = f"{post.title} {post.selftext}"
            sentiment, score = analyze_sentiment(text)
            results.append({
                "Platform": "Reddit",
                "Query": query,
                "Title": post.title,
                "Posted Date": datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
                "Link": post.url,
                "Sentiment": sentiment,
                "Sentiment Percent": score
            })
    
   df =  pd.DataFrame(results).drop_duplicates(subset=["Title", "Link"])
   print(f"✅ {len(df)} Reddit posts found.")
   return df

# ------------------------
# Combined Function for Streamlit
# ------------------------
def get_combined_data(query, entity_type="topic"):
    queries = get_search_queries(entity_type, query)
    news_df = search_news(queries["news"], query)
    reddit_df = search_reddit(queries["reddit"], query)
    combined_df = pd.concat([news_df, reddit_df], ignore_index=True)
    return combined_df
