from langchain.prompts import PromptTemplate


AGGREGATE_PROMPT = PromptTemplate(
    input_variables=["ticker", "history", "macd_data", "rsi_data", "news_data", "fundamental_indicators", "broad_market_indicators"],
    template="""
Context: You are a long term retail investor from India investing in stocks with good fundamentals and growth, you are trying to analyze this stock.
Q: Given the 7-day price history and recent news for the stock {ticker} below, analyze the trend and predict if the stock will likely go up or down tomorrow.

Broad market indicators for Indian Stock Market:
{broad_market_indicators}

Fundamental Indicators for {ticker}:
{fundamental_indicators}

Stock History for {ticker}:
{history}

MACD data for {ticker} for the same timeframe as stock history:
{macd_data}

RSI data for {ticker} for the same timeframe as stock history:
{rsi_data}

Recent News for {ticker}:
{news_data}

Based on both the price history and recent news, provide your analysis. Consider how the news might impact the stock price.

A: Providing a nuanced answer by evaluating both bearish and bullish signals, looking at a larger timeframe as a long term investor we find that 
"""
)


NEWS_PROMPT = PromptTemplate(
        input_variables=["stock_name", "announcement_data"],
        template="""
Analyze the following recent announcements for {stock_name} and provide a comprehensive analysis of each announcement including any PDF content extracted from the announcements.

Announcement Data:
{announcement_data}

For each announcement, please provide:
1. The date of the article published
2. A summary of the announcement content
3. Key dates, metrics, and figures mentioned in the announcement
4. Comparative importance or weight of the news as a rating (1-10, where 10 is most important)

Focus on:
- Financial metrics and performance data
- Regulatory announcements
- Corporate actions (dividends, splits, mergers, etc.)
- Management changes
- Market-related information

Format your response in a clear, structured manner with clear sections for each announcement.The response lenght is proportional to the importance of the news.
    """
    )

