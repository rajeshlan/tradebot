import ccxt
import pandas as pd
import ta
from synchronize_exchange_time import synchronize_time
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
    time_offset = synchronize_time(exchange, 'pool.ntp.org')
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
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)
    df['MACD'] = ta.trend.macd(df['close'])
    df['MACD_signal'] = ta.trend.macd_signal(df['close'])
    df['MACD_diff'] = ta.trend.macd_diff(df['close'])
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

# Calculate performance metrics
def calculate_performance_metrics(df, balance, btc_balance, initial_balance):
    final_balance = balance + btc_balance * df['close'].iloc[-1]
    total_return = (final_balance - initial_balance) / initial_balance
    max_drawdown = ((df['close'].cummax() - df['close']).max()) / df['close'].cummax().max()
    logging.info(f"Final Balance: {final_balance} USDT")
    logging.info(f"Total Return: {total_return * 100:.2f}%")
    logging.info(f"Max Drawdown: {max_drawdown * 100:.2f}%")

# Backtesting function
def backtest_strategy(df):
    balance = 1000
    initial_balance = balance
    btc_balance = 0
    for i in range(len(df)):
        if df['signal'][i] == 'buy' and balance > 0:
            btc_balance = balance / df['close'][i]
            balance = 0
            logging.info(f"Buy BTC at {df['close'][i]}")
        elif df['signal'][i] == 'sell' and btc_balance > 0:
            balance = btc_balance * df['close'][i]
            btc_balance = 0
            logging.info(f"Sell BTC at {df['close'][i]}")
    
    calculate_performance_metrics(df, balance, btc_balance, initial_balance)

# Fetch data, calculate indicators, apply strategy, and backtest
try:
    df = fetch_ohlcv('BTC/USDT', '1d', 365)
    df = calculate_indicators(df)
    df = trading_strategy(df)
    backtest_strategy(df)
except ccxt.BaseError as e:
    logging.error(f"An error occurred: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
