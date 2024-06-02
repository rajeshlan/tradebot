import ccxt
import pandas as pd
import time
import logging
from synchronize_time import synchronize_time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize exchange and synchronize time
def initialize_exchange(api_key, api_secret):
    try:
        exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        logging.info("Initialized Bybit exchange")
        return exchange
    except Exception as e:
        logging.error("Failed to initialize exchange: %s", e)
        raise e

def synchronize_exchange_time(exchange):
    try:
        time_offset = synchronize_time(exchange)
        logging.info("Time synchronized with offset: %d", time_offset)
        return time_offset
    except ccxt.BaseError as e:
        logging.error("Time synchronization failed: %s", e)
        raise e

# Function to fetch historical data
def fetch_ohlcv(exchange, symbol, timeframe='1h', limit=100, time_offset=0):
    try:
        params = {
            'recvWindow': 10000,
            'timestamp': int(time.time() * 1000 + time_offset)
        }
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params=params)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        logging.info("Fetched OHLCV data")
        return df
    except ccxt.BaseError as e:
        logging.error("Failed to fetch OHLCV data: %s", e)
        raise e

# Function to calculate indicators
def calculate_indicators(df):
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    logging.info("Calculated SMA indicators")
    return df

# Define the trading strategy
def trading_strategy(df):
    signals = ['hold']
    for i in range(1, len(df)):
        if df['SMA_50'][i] > df['SMA_200'][i] and df['SMA_50'][i-1] <= df['SMA_200'][i-1]:
            signals.append('buy')
        elif df['SMA_50'][i] < df['SMA_200'][i] and df['SMA_50'][i-1] >= df['SMA_200'][i-1]:
            signals.append('sell')
        else:
            signals.append('hold')
    df['signal'] = signals
    logging.info("Applied trading strategy")
    return df

# Function to place an order
def place_order(exchange, symbol, order_type, side, amount, price=None):
    try:
        order = exchange.create_order(symbol, order_type, side, amount, price)
        logging.info("Placed order: %s", order)
        return order
    except ccxt.BaseError as e:
        logging.error("Failed to place order: %s", e)
        raise e

# Function to execute the trading strategy
def execute_trading_strategy(exchange, df):
    for i in range(len(df)):
        if df['signal'][i] == 'buy':
            logging.info("Buy Signal - Placing Buy Order")
            # Uncomment the following line to actually place the order
            # place_order(exchange, 'BTC/USDT', 'market', 'buy', 0.001)
        elif df['signal'][i] == 'sell':
            logging.info("Sell Signal - Placing Sell Order")
            # Uncomment the following line to actually place the order
            # place_order(exchange, 'BTC/USDT', 'market', 'sell', 0.001)

# Main function to run the trading strategy
def main():
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    
    exchange = initialize_exchange(api_key, api_secret)
    time_offset = synchronize_exchange_time(exchange)

    try:
        df = fetch_ohlcv(exchange, 'BTC/USDT', time_offset=time_offset)
        df = calculate_indicators(df)
        df = trading_strategy(df)
        execute_trading_strategy(exchange, df)
    except ccxt.BaseError as e:
        logging.error("An error occurred during trading: %s", e)

if __name__ == "__main__":
    main()
