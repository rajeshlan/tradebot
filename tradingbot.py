import ccxt
import pandas as pd
import pandas_ta as ta
import time
import logging
import ntplib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to synchronize time with an NTP server
def synchronize_time(ntp_server='time.google.com', max_retries=3, backoff_factor=1):
    client = ntplib.NTPClient()
    retries = 0
    while retries < max_retries:
        try:
            response = client.request(ntp_server)
            offset = response.offset
            logging.info(f"Time synchronized with {ntp_server}. Offset: {offset} seconds")
            return offset
        except ntplib.NTPException as e:
            logging.warning(f"Failed to synchronize time on attempt {retries + 1} with {ntp_server}: {e}")
            retries += 1
            time.sleep(backoff_factor * retries)  # Exponential backoff
    logging.error(f"Max retries ({max_retries}) reached. Unable to synchronize time with {ntp_server}.")
    return 0  # Return 0 offset if synchronization fails

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

# Calculate technical indicators using pandas_ta
def calculate_indicators(df):
    df['SMA50'] = ta.sma(df['close'], length=50)
    df['SMA200'] = ta.sma(df['close'], length=200)
    df['EMA12'] = ta.ema(df['close'], length=12)
    df['EMA26'] = ta.ema(df['close'], length=26)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['RSI'] = ta.rsi(df['close'], length=14)
    df['SAR'] = ta.sar(df['high'], df['low'], df['close'])
    return df

# Generate buy/sell signals
def generate_signals(df):
    df['Buy_Signal'] = (df['close'] > df['SMA50']) & (df['SMA50'] > df['SMA200']) & (df['MACD'] > df['MACD_signal']) & (df['RSI'] < 70)
    df['Sell_Signal'] = (df['close'] < df['SMA50']) & (df['SMA50'] < df['SMA200']) & (df['MACD'] < df['MACD_signal']) & (df['RSI'] > 30)
    return df

# Function to place an order with risk management (stop loss and take profit)
def place_order_with_risk_management(exchange, symbol, side, amount, stop_loss_pct, take_profit_pct):
    try:
        # Place market order
        order = exchange.create_order(symbol, 'market', side, amount)
        price = order['price']

        # Calculate stop loss and take profit prices
        if side == 'buy':
            stop_loss_price = price * (1 - stop_loss_pct)
            take_profit_price = price * (1 + take_profit_pct)
            stop_loss_side = 'sell'
            take_profit_side = 'sell'
        else:
            stop_loss_price = price * (1 + stop_loss_pct)
            take_profit_price = price * (1 - take_profit_pct)
            stop_loss_side = 'buy'
            take_profit_side = 'buy'

        # Place stop loss and take profit orders
        exchange.create_order(symbol, 'stop', stop_loss_side, amount, stop_loss_price)
        exchange.create_order(symbol, 'limit', take_profit_side, amount, take_profit_price)

        logging.info(f"Placed {side} order for {amount} {symbol} at {price} with stop loss at {stop_loss_price} and take profit at {take_profit_price}")

    except Exception as e:
        logging.error(f"Failed to place order with risk management: {e}")
        raise e

# Execute trades
def execute_trades(exchange, df):
    position = None
    stop_loss = None
    take_profit = None
    
    for i in range(len(df)):
        if df['Buy_Signal'].iloc[i] and position is None:
            position = 'long'
            stop_loss = df['close'].iloc[i] * 0.95
            take_profit = df['close'].iloc[i] * 1.10
            logging.info(f"Buy at {df['close'].iloc[i]}, Stop Loss: {stop_loss}, Take Profit: {take_profit}")
            place_order_with_risk_management(exchange, 'BTC/USDT', 'buy', 0.001, 0.05, 0.10)
        
        elif df['Sell_Signal'].iloc[i] and position == 'long':
            position = None
            logging.info(f"Sell at {df['close'].iloc[i]}")
            place_order_with_risk_management(exchange, 'BTC/USDT', 'sell', 0.001, 0.05, 0.10)
        
        elif position == 'long' and df['close'].iloc[i] <= stop_loss:
            position = None
            logging.info(f"Stop Loss Hit at {df['close'].iloc[i]}")
            place_order_with_risk_management(exchange, 'BTC/USDT', 'sell', 0.001, 0.05, 0.10)
        
        elif position == 'long' and df['close'].iloc[i] >= take_profit:
            position = None
            logging.info(f"Take Profit Hit at {df['close'].iloc[i]}")
            place_order_with_risk_management(exchange, 'BTC/USDT', 'sell', 0.001, 0.05, 0.10)

# Main function to run the trade bot
def run_trade_bot(api_key, api_secret):
    try:
        # Initialize exchange
        exchange = initialize_exchange(api_key, api_secret)
        
        # Fetch data
        df = fetch_data(exchange)
        
        # Calculate indicators
        df = calculate_indicators(df)
        
        # Generate signals
        df = generate_signals(df)
        
        # Execute trades
        execute_trades(exchange, df)
        
        # Print first few rows of data
        print(df.head())
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    run_trade_bot(api_key, api_secret)
