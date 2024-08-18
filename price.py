import ccxt
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz
import os

# Initialize the exchange (Binance in this case)
exchange = ccxt.binance()

# Define the UTC time zone
utc_tz = pytz.timezone('UTC')

# Get live price of Bitcoin
def get_live_price():
    try:
        ticker = exchange.fetch_ticker('BTC/USDT')
        live_price = ticker['last']
    except ccxt.NetworkError as e:
        print(f"Network error: {e}")
        live_price = None  # Handle the error by setting live_price to None or take other actions
    return live_price

# Get historical Bitcoin data using yfinance
def get_historical_data(timeframe='1d', period='5y'):  # Adjust period based on interval
    try:
        btc_data = yf.download(tickers='BTC-USD', period=period, interval=timeframe)
        if btc_data.empty:
            raise ValueError(f"No data returned for {timeframe}.")
        return btc_data
    except Exception as e:
        print(f"Failed to download data for {timeframe}: {e}")
        return None

# Adjusted timeframes to fetch with valid periods
timeframes = {
    '1d': '5y',  # Daily data for 5 years
    '1h': '2y',  # Hourly data for the last 2 years
    '15m': '1mo',  # 15-minute data for the last month
    '5m': '1mo',  # 5-minute data for the last month
    '1m': '5d',  # 1-minute data for the last 5 days
    '1wk': '5y',  # Weekly data for the last 5 years
    '1mo': '10y'  # Monthly data for the last 10 years
}

# Dictionary to hold historical data
historical_data = {}

# Initial data fetch and save to Excel
file_path = '/Users/majidahangari/env/bitcoin_data_utc.xlsx'
for timeframe, period in timeframes.items():
    data = get_historical_data(timeframe=timeframe, period=period)
    if data is not None:
        if data.index.tz is None:
            data.index = data.index.tz_localize('UTC')
        else:
            data.index = data.index.tz_convert(utc_tz)
        data.index = data.index.tz_localize(None)
        historical_data[timeframe] = data

with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
    for timeframe, data in historical_data.items():
        data.to_excel(writer, sheet_name=f'Historical {timeframe}', index=True)

print(f"Initial data has been saved to {file_path}")

# Infinite loop to update the Excel file every minute
while True:
    # Get the live Bitcoin price
    live_price = get_live_price()

    # Get the current time in UTC
    current_time = datetime.now(utc_tz).strftime('%Y-%m-%d %H:%M:%S')

    # Update the historical data for each timeframe
    for timeframe, period in timeframes.items():
        data = get_historical_data(timeframe=timeframe, period=period)
        if data is not None:
            if data.index.tz is None:
                data.index = data.index.tz_localize('UTC')
            else:
                data.index = data.index.tz_convert(utc_tz)
            data.index = data.index.tz_localize(None)
            historical_data[timeframe] = data

    # Load or create the live price DataFrame
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_excel(file_path, sheet_name='Live Price')
        except ValueError:
            existing_data = pd.DataFrame(columns=['Live Price', 'Timestamp'])
        new_data = pd.DataFrame({'Live Price': [live_price], 'Timestamp': [current_time]})
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = pd.DataFrame({'Live Price': [live_price], 'Timestamp': [current_time]})

    # Save the updated data back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for timeframe, data in historical_data.items():
            data.to_excel(writer, sheet_name=f'Historical {timeframe}', index=True)
        updated_data.to_excel(writer, sheet_name='Live Price', index=False)

    print(f"Data has been updated at {current_time} UTC")

    # Wait for 60 seconds (1 minute) before the next update
    time.sleep(60)
