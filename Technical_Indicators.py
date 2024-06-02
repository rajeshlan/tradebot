import ccxt
import pandas as pd
import pandas_ta as ta
import time
import logging
import ntplib

# Function to synchronize time with an NTP server
def synchronize_time():
    client = ntplib.NTPClient()
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = client.request('time.google.com')
            offset = response.offset
            return offset
        except ntplib.NTPException as e:
            logging.warning("Failed to synchronize time: %s", e)
            retries += 1
            time.sleep(1)  # Wait for a short duration before retrying
    logging.error("Max retries reached. Unable to synchronize time.")
    return 0  # Return 0 offset if synchronization fails

# Initialize the Bybit exchange
def initialize_exchange(api_key, api_secret):
    try:
        exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,  # This helps to avoid rate limit errors
        })
        logging.info("Initialized Bybit exchange")
        return exchange
    except Exception as e:
        logging.error("Failed to initialize exchange: %s", e)
        raise e

# Function to fetch historical data
def fetch_ohlcv(exchange, symbol, timeframe='1h', limit=100, time_offset=0):
    params = {
        'recvWindow': 10000,  # Increased to 10000 milliseconds (10 seconds)
        'timestamp': int(time.time() * 1000 + time_offset)
    }
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params=params)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except ccxt.BaseError as e:
        logging.error("Error fetching OHLCV data: %s", e)
        raise e

# Function to calculate indicators
def calculate_indicators(df):
    df['SMA_50'] = df.ta.sma(length=50)
    df['SMA_200'] = df.ta.sma(length=200)
    return df

# Define the trading strategy
def trading_strategy(df):
    signals = ['hold']  # Initialize with 'hold' for the first entry
    for i in range(1, len(df)):
        if df['SMA_50'][i] > df['SMA_200'][i] and df['SMA_50'][i-1] <= df['SMA_200'][i-1]:
            signals.append('buy')
        elif df['SMA_50'][i] < df['SMA_200'][i] and df['SMA_50'][i-1] >= df['SMA_200'][i-1]:
            signals.append('sell')
        else:
            signals.append('hold')
    df['signal'] = signals
    return df

# Main function to orchestrate the workflow
def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Replace with your actual API credentials
    API_KEY = 'YOUR_API_KEY'
    API_SECRET = 'YOUR_API_SECRET'
    
    try:
        # Attempt time synchronization
        time_offset = synchronize_time()
        logging.info("Time synchronized with offset: %d", time_offset)
        
        # Initialize exchange
        exchange = initialize_exchange(API_KEY, API_SECRET)
        
        # Fetch data, calculate indicators, apply strategy
        df = fetch_ohlcv(exchange, 'BTC/USDT', time_offset=time_offset)
        df = calculate_indicators(df)
        df = trading_strategy(df)
        
        # Output the resulting DataFrame
        print(df.tail())
        
    except Exception as e:
        logging.error("An error occurred during the main execution: %s", e)

# Run the main function
if __name__ == "__main__":
    main()
