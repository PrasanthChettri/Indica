import os
import re
import praw
from collections import defaultdict
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# --- Load Gemini ---

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# --- Prompt template ---
prompt = ChatPromptTemplate.from_template("""
Given the following Reddit post content:

"{post_text}"

Classify the sentiment toward Indian stocks as one of:
- Bullish (positive or optimistic sentiment)
- Bearish (negative or pessimistic sentiment)
- Neutral (no strong emotion or mixed)

Respond in format:
Sentiment: <Bullish/Bearish/Neutral>
Reason: <short explanation of one line>
""")

# --- Reddit API config ---
secret = os.getenv("REDDIT_SECRET")
client_id = os.getenv("REDDIT_CLIENT")
reddit = praw.Reddit(
    client_id=client_id, 
    client_secret=secret,
    user_agent="StockSentimentApp by /u/edgyboi696969"
)

subreddit = reddit.subreddit("IndianStockMarket")
posts = subreddit.hot(limit=100)

# --- Pattern to extract stock-like tickers (uppercase) ---
stock_sentiment = []

for post in posts:
    if (not post.link_flair_text) or post.link_flair_text.lower() != "news":
        continue

    content = (post.title or "") + " " + (post.selftext or "")

    try:
        chain = prompt | llm
        result = chain.invoke({"post_text": content})
        print(f"🧵 Post: {post.title}")
        print(result.content.strip())

        sentiment_line = result.content.strip().splitlines()[0]
        if "Bullish" in sentiment_line:
            sentiment = "Bullish"
        elif "Bearish" in sentiment_line:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

        stock_sentiment.append(sentiment)

    except Exception as e:
        print(f"Error analyzing post: {e}")

# --- Aggregate summary ---
print("\n📊 Sentiment Summary:")
