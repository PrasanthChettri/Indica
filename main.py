import datetime
from dotenv import load_dotenv, find_dotenv
from ohvc import get_stock_analysis
import prompts
load_dotenv(find_dotenv())

import os
import yfinance as yf
import pprint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prettytable import PrettyTable
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import requests
import json
import pandas as pd
from news import get_announcements
from gemini import Gemini
from stubs import get_stub_predictions, get_stub_error_response, get_stub_loading_response
import time

# Load the model (Gemini via LangChain)

# Define a prompt template that includes news data

# Create the chain
chain = Gemini().get_chain(prompts.AGGREGATE_PROMPT)

# Fetch stock data (last 7 days for example)
async def predict_stock(name, ticker):
    ohvc = get_stock_analysis(ticker)
    
    # Get news data for the stock
    news_data = await get_announcements(ticker)
    
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: chain.invoke({
        "ticker": ticker, 
        "history": ohvc["weekly_close"], 
        "macd_data": ohvc["macd_data"], 
        "rsi_data": ohvc["rsi_data"], 
        "news_data": news_data,
        "fundamental_indicators": ohvc["fundamental_indicators"],
        "broad_market_indicators": ohvc["broad_market_indicators"],
        "current_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }))
    return {
        "stock_name": name,
        "ticker": ticker,
        "prediction": response['text'],
        "news_impact": news_data,
    }

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of Indian stocks with their NSE tickers
stocks = {
    "Tata Motors": "TATAMOTORS.NS"
}


@app.get("/predictions")
async def get_predictions():
    tasks = [predict_stock(name, ticker) for name, ticker in stocks.items()]
    results = await asyncio.gather(*tasks)
    
    return JSONResponse(content={
        "predictions": results 
    })

@app.get("/predictions/stub")
async def get_predictions_stub():
    """
    Stub API endpoint for testing predictions without requiring AI models or external APIs.
    Returns mock data that mimics the structure of real predictions.
    """
    #sumulate processing time with three second delay
    time.sleep(3)
    return JSONResponse(content=get_stub_predictions())

@app.get("/")
async def get_index():
    return FileResponse("templates/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
