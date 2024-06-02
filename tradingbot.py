import ccxt
import pandas as pd
import time
import logging
import ntplib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to synchronize time with an NTP server
def synchronize_time():
    client = ntplib.NTPClient()
    MAX_RETRIES = 3
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = client.request('time.google.com')
            offset = int((response.tx_time - time.time()) * 1000)  # Convert offset to milliseconds
            return offset
        except ntplib.NTPException as e:
            logging.warning("Failed to synchronize time: %s", e)
            retries += 1
            time.sleep(1)  # Wait for a short duration before retrying
    logging.error("Max retries reached. Unable to synchronize time.")
    raise ccxt.BaseError("Failed to synchronize time with NTP server")

# Function to initialize the Bybit exchange
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

# Fetch data for BTC/USDT
def fetch_data(exchange, symbol='BTC/USDT'):
    try:
        params = {
            'recvWindow': 10000,
            'timestamp': int(time.time() * 1000 + synchronize_time())
        }
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100, params=params)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        logging.info("Fetched OHLCV data for %s", symbol)
        return df
    except Exception as e:
        logging.error("An error occurred while fetching data: %s", e)
        raise e

# Example usage
try:
    # Initialize exchange
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    exchange = initialize_exchange(api_key, api_secret)

    # Fetch data
    df = fetch_data(exchange)

    # Print first few rows of data
    print(df.head())
except Exception as e:
    print(f"An error occurred: {e}")
