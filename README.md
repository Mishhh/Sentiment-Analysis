# 🧠 Reddit & News Sentiment Analysis Dashboard

Analyze public sentiment around any topic using **Reddit posts** and **Google News articles** — all in one interactive dashboard powered by **Streamlit**, **VADER Sentiment Analysis**, and **PRAW**.

🔗 **Live Demo:** [View on Streamlit](https://sentiment-analysis-aappttu35ub9cg3zbbdnuqb.streamlit.app/)

---

## 🚀 Project Overview

This project performs **real-time sentiment analysis** on Reddit discussions and news headlines related to a given keyword.  
It helps understand **how people feel about specific topics**, brands, or events by analyzing textual content and classifying it as **Positive**, **Negative**, or **Neutral**.

### ✨ Key Features
- 🔍 Fetches latest **Reddit posts** and **Google News articles** for any search keyword.  
- 💬 Performs sentiment analysis using **VADER (NLTK)**.  
- 📊 Displays interactive visualizations to compare sentiments across platforms.  
- ⚡ Real-time data processing using **PRAW** and **Google News RSS**.  
- 💾 Option to export sentiment data as CSV.  
- 🌐 Hosted on Streamlit Cloud for instant access.

---

## 🧩 Tech Stack

| Category | Tools Used |
|-----------|-------------|
| Language | Python |
| Libraries | Streamlit, Pandas, Plotly, NLTK (VADER), PRAW, Requests, LXML |
| Data Sources | Reddit API, Google News RSS |
| Deployment | Streamlit Cloud |

---


## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/reddit-sentiment-analysis.git
cd reddit-sentiment-analysis
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
source venv/bin/activate   # For Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Reddit API credentials
  - Create a .env file in the project root and add:
```bash
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=reputation_analysis_script
```

### 5. Run the Streamlit app
```bash
streamlit run app.py
```

---

## 📈 Dashboard Preview



## 🧮 How Sentiment Is Calculated

  - Each Reddit post or News headline is analyzed using VADER Sentiment Analyzer, which outputs a compound score between -1 and +1:

  |Score Range |	Sentiment Type |
  |------------|-----------------|
  |> 0.05	| Positive 😀 |
  |< -0.05	| Negative 😞 |
  |-0.05 to 0.05 |	Neutral 😐 |
