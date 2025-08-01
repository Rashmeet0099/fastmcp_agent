import os
import requests
import json
import pandas as pd

# Load API key from environment variables
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_stock_data(symbol: str, outputsize: str = "compact") -> str:
    """Fetches daily stock time series data for a given stock symbol.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        outputsize (str): The size of the data output. 'compact' returns the last 100 days. 'full' returns the full time series.
        
    Returns:
        str: A JSON string of the stock data, or an error message.
    """
    if not API_KEY:
        return "Error: Alpha Vantage API key is not set."
    
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY,
        'outputsize': outputsize,
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "Time Series (Daily)" in data:
            # The API returns a nested dictionary; we need to flatten it
            time_series = data["Time Series (Daily)"]
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index.name = 'Date'
            
            # Rename columns for clarity and convert to float
            df.columns = [col.split('. ')[1] for col in df.columns]
            df = df.astype(float)
            
            return df.to_json(orient='records')
        else:
            return f"Error fetching stock data for {symbol}: {data.get('Note', 'Check the symbol and API key.')}"
    
    except Exception as e:
        return f"An error occurred while fetching data: {e}"
