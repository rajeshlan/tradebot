import ccxt
import pandas as pd
import ta
from synchronize_time import synchronize_time
import logging
import time

# Setup logging if not already set up
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Bybit exchange
exchange = ccxt.bybit({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_API_SECRET',
    'enableRateLimit': True,
    'options': {
        'adjustForTimeDifference': True,
        'recvWindow': 10000,
    }
})

# Synchronize time with the exchange
try:
    time_offset = synchronize_time(exchange)
    logging.info("Time synchronized with offset: %d", time_offset)
except ccxt.BaseError as e:
    logging.error("Time synchronization failed: %s", e)
    exit()

# Function to fetch historical data
def fetch_ohlcv(symbol, timeframe='1d', limit=365):
    params = {
        'recvWindow': 10000,
        'timestamp': int(time.time() * 1000 + time_offset)
    }
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params=params)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Calculate moving averages
def calculate_indicators(df):
    df['SMA_50'] = ta.trend.sma_indicator(df['close'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(df['close'], window=200)
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
    return df

# Backtesting function
def backtest_strategy(df):
    balance = 1000
    btc_balance = 0
    for i in range(len(df)):
        if df['signal'][i] == 'buy' and balance > 0:
            btc_balance = balance / df['close'][i]
            balance = 0
            print(f"Buy BTC at {df['close'][i]}")
        elif df['signal'][i] == 'sell' and btc_balance > 0:
            balance = btc_balance * df['close'][i]
            btc_balance = 0
            print(f"Sell BTC at {df['close'][i]}")
    
    final_balance = balance + btc_balance * df['close'].iloc[-1]
    print(f"Final Balance: {final_balance} USDT")

# Fetch data, calculate indicators, apply strategy, and backtest
try:
    df = fetch_ohlcv('BTC/USDT', '1d', 365)
    df = calculate_indicators(df)
    df = trading_strategy(df)
    backtest_strategy(df)
except ccxt.BaseError as e:
    print(f"An error occurred: {e}")
