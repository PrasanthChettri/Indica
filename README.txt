INDICA - AI-POWERED INDIAN STOCK MARKET ANALYSIS SYSTEM
========================================================

PROJECT OVERVIEW
----------------
Indica is a comprehensive AI-driven stock analysis platform that combines technical indicators, fundamental analysis, and real-time news sentiment to provide intelligent stock predictions for Indian markets. The system leverages multiple AI models and data sources to deliver actionable investment insights.

TECHNICAL STACK
---------------
• Backend: Python, FastAPI, Uvicorn
• AI/ML: LangChain, Google Gemini AI, OpenAI
• Data Sources: Yahoo Finance (yfinance), Indian Stock APIs, News APIs
• Technical Analysis: pandas-ta, NumPy, Pandas
• Data Processing: PDF extraction (pdfplumber), Web scraping (BeautifulSoup, Selenium)
• Real-time Data: Reddit sentiment analysis, News sentiment analysis

KEY FEATURES & CAPABILITIES
---------------------------
1. MULTI-MODEL AI ANALYSIS
   - Integrated Google Gemini AI for comprehensive stock analysis
   - LangChain framework for prompt engineering and chain management
   - Custom prompt templates for specialized analysis scenarios

2. TECHNICAL INDICATORS ANALYSIS
   - MACD (Moving Average Convergence Divergence) calculations
   - RSI (Relative Strength Index) analysis
   - Weekly and daily price trend analysis
   - Broad market indicators (Nifty, Sensex, VIX, Bank Nifty)

3. FUNDAMENTAL ANALYSIS
   - P/E ratios, Price-to-Book, Price-to-Sales ratios
   - Dividend yield analysis
   - Market capitalization and enterprise value
   - Debt-to-equity and return on equity metrics
   - 52-week high/low analysis

4. REAL-TIME NEWS & SENTIMENT ANALYSIS
   - Automated PDF extraction and analysis from BSE announcements
   - News sentiment analysis using AI models
   - Reddit stock sentiment analysis
   - Real-time news impact assessment

5. REST API DEVELOPMENT
   - FastAPI-based RESTful API with CORS support
   - Asynchronous processing for concurrent stock analysis
   - JSON response formatting for frontend integration
   - Scalable architecture for multiple stock analysis

6. DATA PROCESSING & EXTRACTION
   - Automated PDF text and table extraction
   - Web scraping for real-time data collection
   - Multi-source data aggregation and normalization
   - Error handling and data validation

TECHNICAL HIGHLIGHTS
--------------------
• Implemented custom technical indicators using pandas-ta
• Developed PDF extraction pipeline for BSE announcements
• Created modular AI analysis chains using LangChain
• Built RESTful API with FastAPI for frontend integration
• Integrated multiple data sources with error handling
• Implemented asynchronous processing for concurrent analysis
