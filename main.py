import datetime
from dotenv import load_dotenv, find_dotenv
from ohvc import get_stock_analysis
import prompts
load_dotenv(find_dotenv())

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from news import get_announcements
from gemini import Gemini
from stubs import get_stub_predictions
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

@app.get("/prediction")
async def get_predictions(name: str, ticker: str):
    return await predict_stock(name, ticker)


@app.get("/prediction/stub")
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
    return FileResponse("frontend/index.html")

@app.get("/styles")
async def get_css():
    return FileResponse("frontend/styles.css")

@app.get("/js")
async def get_js():
    FRONT_END_JS_FILES = ["frontend/fetcher.js", "frontend/utils.js"]
    js_content = ""
    for file in FRONT_END_JS_FILES :
        fb = open(file)
        js_content += fb.read() + "\n"
        fb.close() 
    return Response(content=js_content, media_type="application/javascript")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
