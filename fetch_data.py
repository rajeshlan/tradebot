import ccxt
import pandas as pd
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def synchronize_time_with_exchange(exchange):
    try:
        server_time = exchange.milliseconds()
        local_time = int(time.time() * 1000)
        time_offset = server_time - local_time
        logging.info("Time synchronized with exchange. Offset: %d milliseconds", time_offset)
        return time_offset
    except ccxt.BaseError as sync_error:
        logging.error("Failed to synchronize time with exchange: %s", sync_error)
        raise sync_error

def fetch_data(exchange, symbol='BTC/USDT'):
    try:
        # Synchronize time with exchange
        time_offset = synchronize_time_with_exchange(exchange)
        
        # Fetch OHLCV data
        params = {
            'recvWindow': 10000,  # Adjust recvWindow as needed
            'timestamp': exchange.milliseconds() + time_offset
        }
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100, params=params)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        logging.info("Fetched OHLCV data for %s", symbol)
        return df
    except ccxt.BaseError as ccxt_error:
        logging.error("An error occurred while fetching data: %s", ccxt_error)
        raise ccxt_error
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise e

# Example usage
if __name__ == "__main__":
    # Initialize exchange
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    exchange = ccxt.bybit({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,  # This helps to avoid rate limit errors
    })

    try:
        # Fetch data
        df = fetch_data(exchange)

        # Print first few rows of data
        print(df.head())
    except ccxt.NetworkError as net_error:
        logging.error("A network error occurred: %s", net_error)
        # Retry or handle the error as needed
    except ccxt.BaseError as error:
        logging.error("An error occurred: %s", error)
