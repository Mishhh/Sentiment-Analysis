import streamlit as st
import pandas as pd
import plotly.express as px
from sentiment_analysis import get_combined_data

# ------------------------#
# Page Configuration
# ------------------------#
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    layout="wide",
    page_icon="📊",
)

# ------------------------#
# Header
# ------------------------#
st.title("📊 Sentiment Analysis Dashboard")
st.markdown(
    """
    Gain insights into public sentiment from **Reddit** and **Google News** — all in one place.  
    Enter a keyword to uncover opinions, discussions, and media coverage about your topic of interest.
    """
)
st.markdown("---")

# ------------------------#
# Sidebar Controls
# ------------------------#
st.sidebar.header("🔍 Search Settings")
query = st.sidebar.text_input(
    "Enter a topic or brand name", 
    placeholder="e.g., Zomato / Tesla / Climate Change"
)
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tip: Broader keywords fetch more results. For example, use *Electric Cars* instead of *Tesla Model 3*."
)

# ------------------------#
# Run Analysis
# ------------------------#
if st.sidebar.button("Analyze Sentiment"):
    if not query:
        st.warning("⚠️ Please enter a topic or keyword before analyzing.")
    else:
        with st.spinner("🔎 Collecting and analyzing data... Please wait ⏳"):
            df = get_combined_data(query)

        if df.empty:
            st.error("❌ No data found. Try another keyword.")
        else:
            st.success(f"✅ Analysis completed for **{query.title()}**!")

            # ------------------------#
            # Clean & Prepare Data
            # ------------------------#
            df["Published Date"] = pd.to_datetime(df.get("Published Date"), errors='coerce')
            df["Posted Date"] = pd.to_datetime(df.get("Posted Date"), errors='coerce')
            df["Date"] = df["Published Date"].combine_first(df["Posted Date"])
            df.dropna(subset=["Date"], inplace=True)
            df["Month"] = df["Date"].dt.to_period("M").astype(str)

            # ------------------------#
            # Key Metrics
            # ------------------------#
            sentiment_counts = df["Sentiment"].value_counts()
            total_records = len(df)

            st.markdown("### 📊 Overview Metrics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📰 Total Mentions", total_records)
            col2.metric("😊 Positive", sentiment_counts.get("Positive", 0))
            col3.metric("😐 Neutral", sentiment_counts.get("Neutral", 0))
            col4.metric("😡 Negative", sentiment_counts.get("Negative", 0))

            st.markdown("---")

            # ------------------------#
            #  Sentiment Distribution
            # ------------------------#
            st.subheader("💬 Sentiment Distribution")

            sentiment_df = sentiment_counts.reset_index()
            sentiment_df.columns = ["Sentiment", "Count"]

            fig1 = px.bar(
                sentiment_df,
                x="Sentiment",
                y="Count",
                color="Sentiment",
                text_auto=True,
                color_discrete_map={
                    "Positive": "#2ecc71",
                    "Neutral": "#95a5a6",
                    "Negative": "#e74c3c",
                },
                title=f"Sentiment Breakdown for {query.title()}",
            )

            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title_font=dict(size=18, family="Arial Black"),
                showlegend=False,
                margin=dict(l=60, r=60, t=80, b=60),
                yaxis_title="Mentions Count",
            )
            st.plotly_chart(fig1, use_container_width=True)

            # ------------------------#
            # Sentiment Trend Over Time
            # ------------------------#
            st.subheader("📅 Sentiment Trend Over Time")

            trend_df = df.groupby(["Month", "Sentiment"]).size().reset_index(name="Count")

            fig2 = px.area(
                trend_df,
                x="Month",
                y="Count",
                color="Sentiment",
                color_discrete_map={
                    "Positive": "#2ecc71",
                    "Neutral": "#95a5a6",
                    "Negative": "#e74c3c",
                },
                title=f"Monthly Sentiment Trend for {query.title()}",
            )

            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                hovermode="x unified",
                xaxis_title="Month",
                yaxis_title="Mentions",
                legend_title="Sentiment",
                margin=dict(l=60, r=60, t=80, b=60),
            )
            st.plotly_chart(fig2, use_container_width=True)

            # ------------------------#
            #  Platform-wise Comparison
            # ------------------------#
            st.subheader("🌐 Platform-wise Sentiment Comparison")

            col1, col2 = st.columns(2)
            reddit_df = df[df["Platform"].str.lower() == "reddit"]
            news_df = df[df["Platform"].str.lower() == "news"]

            # Reddit Chart
            with col1:
                reddit_sentiment = reddit_df["Sentiment"].value_counts().reset_index()
                reddit_sentiment.columns = ["Sentiment", "Count"]
                fig_r = px.pie(
                    reddit_sentiment,
                    names="Sentiment",
                    values="Count",
                    hole=0.5,
                    color="Sentiment",
                    color_discrete_map={
                        "Positive": "#2ecc71",
                        "Neutral": "#95a5a6",
                        "Negative": "#e74c3c",
                    },
                    title="Reddit Sentiment",
                )
                fig_r.update_traces(textinfo="percent+label", pull=[0.05]*len(reddit_sentiment))
                st.plotly_chart(fig_r, use_container_width=True)

            # News Chart
            with col2:
                news_sentiment = news_df["Sentiment"].value_counts().reset_index()
                news_sentiment.columns = ["Sentiment", "Count"]
                fig_n = px.pie(
                    news_sentiment,
                    names="Sentiment",
                    values="Count",
                    hole=0.5,
                    color="Sentiment",
                    color_discrete_map={
                        "Positive": "#2ecc71",
                        "Neutral": "#95a5a6",
                        "Negative": "#e74c3c",
                    },
                    title="News Sentiment",
                )
                fig_n.update_traces(textinfo="percent+label", pull=[0.05]*len(news_sentiment))
                st.plotly_chart(fig_n, use_container_width=True)

            # ------------------------#
            #  Detailed Data Table
            # ------------------------#
            st.subheader("📋 Detailed Mentions")

            st.dataframe(
                df[["Platform", "Title", "Sentiment", "Sentiment Percent", "Link", "Date"]],
                use_container_width=True,
                height=400,
                hide_index=True,
            )

            # ------------------------#
            #  Footer
            # ------------------------#
            st.markdown("---")
            st.caption(
                "📘 Built with ❤️ using Streamlit | Data Source: Reddit & Google News RSS | Developer: Mishalee Lambat"
            )

else:
    st.info("👈 Enter a keyword in the sidebar and click **Analyze Sentiment** to start.")


