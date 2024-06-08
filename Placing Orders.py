import ccxt
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
from synchronize_exchange_time import synchronize_time

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
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['RSI'] = calculate_rsi(df['close'], 14)
    logging.info("Calculated technical indicators")
    return df

def calculate_rsi(series, period):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Detect patterns
def detect_patterns(df):
    df['HeadAndShoulders'] = detect_head_and_shoulders(df)
    df['DoubleTop'] = detect_double_top(df)
    logging.info("Detected patterns")
    return df

def detect_head_and_shoulders(df):
    pattern = [0] * len(df)
    for i in range(2, len(df) - 1):
        if df['high'][i - 2] < df['high'][i - 1] > df['high'][i] and \
           df['high'][i - 1] > df['high'][i + 1] and \
           df['low'][i - 2] > df['low'][i - 1] < df['low'][i] and \
           df['low'][i - 1] < df['low'][i + 1]:
            pattern[i] = 1
    return pattern

def detect_double_top(df):
    pattern = [0] * len(df)
    for i in range(1, len(df) - 1):
        if df['high'][i - 1] < df['high'][i] > df['high'][i + 1] and \
           df['high'][i] == df['high'][i + 1]:
            pattern[i] = 1
    return pattern

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

# Function to place an order with risk management
def place_order_with_risk_management(exchange, symbol, side, amount, stop_loss, take_profit):
    try:
        # Place market order
        order = exchange.create_order(symbol, 'market', side, amount)
        logging.info(f"Market order placed: {order}")
        
        order_price = order['price'] if 'price' in order else None
        
        if order_price:
            stop_loss_price = order_price * (1 - stop_loss) if side == 'buy' else order_price * (1 + stop_loss)
            take_profit_price = order_price * (1 + take_profit) if side == 'buy' else order_price * (1 - take_profit)

            logging.info(f"Stop Loss: {stop_loss_price}, Take Profit: {take_profit_price}")
            
            # Place stop-loss and take-profit orders
            if side == 'buy':
                exchange.create_order(symbol, 'stop', 'sell', amount, stop_loss_price)
                exchange.create_order(symbol, 'limit', 'sell', amount, take_profit_price)
            else:
                exchange.create_order(symbol, 'stop', 'buy', amount, stop_loss_price)
                exchange.create_order(symbol, 'limit', 'buy', amount, take_profit_price)
            
        else:
            logging.warning("Order price not available, cannot calculate stop-loss and take-profit.")
    except ccxt.BaseError as e:
        logging.error(f"An error occurred: {e}")

# Function to execute the trading strategy
def execute_trading_strategy(exchange, df):
    for i in range(len(df)):
        if df['signal'][i] == 'buy':
            logging.info("Buy Signal - Placing Buy Order")
            # Uncomment the following line to actually place the order
            # place_order_with_risk_management(exchange, 'BTC/USDT', 'buy', 0.001, 0.01, 0.02)
        elif df['signal'][i] == 'sell':
            logging.info("Sell Signal - Placing Sell Order")
            # Uncomment the following line to actually place the order
            # place_order_with_risk_management(exchange, 'BTC/USDT', 'sell', 0.001, 0.01, 0.02)

# Main function to run the trading strategy
def main():
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    
    exchange = initialize_exchange(api_key, api_secret)
    time_offset = synchronize_exchange_time(exchange)

    try:
        df = fetch_ohlcv(exchange, 'BTC/USDT', time_offset=time_offset)
        df = calculate_indicators(df)
        df = detect_patterns(df)
        df = trading_strategy(df)
        execute_trading_strategy(exchange, df)
    except ccxt.BaseError as e:
        logging.error("An error occurred during trading: %s", e)

if __name__ == "__main__":
    main()
