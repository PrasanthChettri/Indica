import yfinance as yf
import pandas_ta as ta
import pandas as pd
import json

# Weekly Close Data
from typing import Dict, Any, Union
import pandas as pd

def get_broad_market_indicators() -> str:
    """
    Get broad market indicators including Nifty, Sensex, and VIX.
    
    Returns:
        str: JSON string containing broad market indicators
    """
    try:
        # Nifty 50
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="5d")
        
        # Sensex
        sensex = yf.Ticker("^BSESN")
        sensex_hist = sensex.history(period="5d")
        
        # India VIX (Volatility Index)
        vix = yf.Ticker("^INDIAVIX")
        vix_hist = vix.history(period="5d")
        
        # Bank Nifty
        bank_nifty = yf.Ticker("^NSEBANK")
        bank_nifty_hist = bank_nifty.history(period="5d")
        
        data = {
            "nifty": {
                "current": round(nifty_hist['Close'].iloc[-1], 2) if not nifty_hist.empty else 'N/A',
                "change": round(nifty_hist['Close'].iloc[-1] - nifty_hist['Close'].iloc[-2], 2) if len(nifty_hist) > 1 else 'N/A',
                "change_percent": round(((nifty_hist['Close'].iloc[-1] - nifty_hist['Close'].iloc[-2]) / nifty_hist['Close'].iloc[-2] * 100), 2) if len(nifty_hist) > 1 else 'N/A'
            },
            "sensex": {
                "current": round(sensex_hist['Close'].iloc[-1], 2) if not sensex_hist.empty else 'N/A',
                "change": round(sensex_hist['Close'].iloc[-1] - sensex_hist['Close'].iloc[-2], 2) if len(sensex_hist) > 1 else 'N/A',
                "change_percent": round(((sensex_hist['Close'].iloc[-1] - sensex_hist['Close'].iloc[-2]) / sensex_hist['Close'].iloc[-2] * 100), 2) if len(sensex_hist) > 1 else 'N/A'
            },
            "vix": {
                "current": round(vix_hist['Close'].iloc[-1], 2) if not vix_hist.empty else 'N/A',
                "change": round(vix_hist['Close'].iloc[-1] - vix_hist['Close'].iloc[-2], 2) if len(vix_hist) > 1 else 'N/A'
            },
            "bank_nifty": {
                "current": round(bank_nifty_hist['Close'].iloc[-1], 2) if not bank_nifty_hist.empty else 'N/A',
                "change": round(bank_nifty_hist['Close'].iloc[-1] - bank_nifty_hist['Close'].iloc[-2], 2) if len(bank_nifty_hist) > 1 else 'N/A',
                "change_percent": round(((bank_nifty_hist['Close'].iloc[-1] - bank_nifty_hist['Close'].iloc[-2]) / bank_nifty_hist['Close'].iloc[-2] * 100), 2) if len(bank_nifty_hist) > 1 else 'N/A'
            }
        }
        #Serialize data into a string with format 
        #Key: 
        #   key: value
        result = ""
        for key, value in data.items():
            result += f"{key}:\n"
            for k, v in value.items():
                result += f"  {k}: {v}\n"
        return result

    except Exception as e:
        print(f"Error getting broad market indicators: {e}")
        return result

def get_stock_fundamental_indicators(ticker: str) -> str:
    """
    Get fundamental indicators for a stock.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        Dict[str, Any]: Dictionary containing fundamental indicators
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        data = {
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "forward_pe": info.get('forwardPE', 'N/A'),
            "price_to_book": info.get('priceToBook', 'N/A'),
            "price_to_sales": info.get('priceToSalesTrailing12Months', 'N/A'),
            "dividend_yield": info.get('dividendYield', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "enterprise_value": info.get('enterpriseValue', 'N/A'),
            "debt_to_equity": info.get('debtToEquity', 'N/A'),
            "return_on_equity": info.get('returnOnEquity', 'N/A'),
            "profit_margins": info.get('profitMargins', 'N/A'),
            "beta": info.get('beta', 'N/A'),
            "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            "avg_volume": info.get('averageVolume', 'N/A'),
            "volume": info.get('volume', 'N/A')
        }
        result = ""
        for key, value in data.items():
            result += f"{key}: {value}\n"
        return result
    except Exception as e:
        print(f"Error getting fundamental indicators: {e}")
        return {}

def get_stock_analysis(ticker: str) -> Dict[str, str]:
    """
    Get comprehensive stock analysis including weekly/daily close data and technical indicators.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "RELIANCE.NS")
    
    Returns:
        Dict[str, Union[pd.Series, pd.DataFrame]]: Dictionary containing analysis data with keys:
            - weekly_close: pd.Series of weekly closing prices
            - daily_close: pd.Series of daily closing prices  
            - macd_data: pd.DataFrame of MACD indicators
            - rsi_data: pd.Series of RSI values
            - combined_analysis: pd.DataFrame of combined technical analysis
    """
    ticker_obj = yf.Ticker(ticker)
    
    # Get weekly data
    hist_weekly = ticker_obj.history(period="10mo", interval="1wk")
    weekly_close: pd.Series = hist_weekly['Close'].map(lambda x: round(x, 2))
    weekly_close.index = weekly_close.index.date
    
    # Get daily data
    hist_daily = ticker_obj.history(period="15d", interval="1d")
    daily_close: pd.Series = hist_daily['Close'].map(lambda x: round(x, 2))
    
    # Calculate technical indicators and get last row
    macd_data: pd.DataFrame = ta.macd(weekly_close, fast=12, slow=26, signal=9)
    macd_data = macd_data.map(lambda x: round(x, 2))
    last_macd_row = macd_data.iloc[[-1]] if not macd_data.empty else None
    print(type(last_macd_row))

    RSI: pd.Series = ta.rsi(weekly_close, length=14)
    last_rsi_value = RSI.iloc[[-1]] if not RSI.empty else None
    last_rsi_value = last_rsi_value.map(lambda x: round(x, 2))

    
    return {
        "weekly_close": weekly_close.to_string(),
        "macd_data": last_macd_row.to_string(),
        "rsi_data": ' '.join(map(str,last_rsi_value.to_list())),
        "broad_market_indicators": get_broad_market_indicators(),
        "fundamental_indicators": get_stock_fundamental_indicators(ticker)
    }
if __name__ == "__main__":
    s =  get_stock_fundamental_indicators("RELIANCE.NS")
    print(s)
    #print(*map(type, s.values()), sep = '\n')