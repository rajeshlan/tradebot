****# tradebot
trying to develop a automated trading bot with python for auto executions with being able to change strategies with time
all these codes has error for time stamps or error while syncing the time server with the code., 
i will keep updating the changes
****


BELOW ARE THE TERMINALS ERROR I HAVE BEEN FACING
I THINK ALL ERROR ARE DUE TO SERVER TIMESTAMP., BUT IF THERE'S ANYONE HERE WHO CAN HELP 
PLEASE GO THROUGH THESE ERROR AND RESOLVE 



PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/tradingbot.py"

2024-06-08 14:52:39,287 - INFO - Initialized Bybit exchange
2024-06-08 14:52:39,372 - INFO - Time synchronized with time.google.com. Offset: 270.07315397262573 seconds
2024-06-08 14:52:39,678 - ERROR - An error occurred while fetching data: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or
recv_window param. req_timestamp[1717838559373],server_timestamp[1717838829693],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838829693}
2024-06-08 14:52:39,678 - ERROR - An error occurred: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window param. r
eq_timestamp[1717838559373],server_timestamp[1717838829693],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838829693}


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/Trading Strategy.p
y"

2024-06-08 14:52:47,445 - INFO - Time synchronized with time.google.com. Offset: 270.07328605651855 seconds
2024-06-08 14:52:47,445 - INFO - Time synchronized with offset: 270
2024-06-08 14:52:47,445 - INFO - Initialized Bybit exchange
2024-06-08 14:52:47,768 - ERROR - Error fetching OHLCV data: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window
param. req_timestamp[1717838567445],server_timestamp[1717838837799],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838837799}
2024-06-08 14:52:47,784 - ERROR - An error occurred during the main execution: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timesta
mp or recv_window param. req_timestamp[1717838567445],server_timestamp[1717838837799],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838837799}


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/test_trading_bot.p
y"

2024-06-08 14:52:54,594 - INFO - Initialized Bybit exchange
.2024-06-08 14:52:54,594 - INFO - Placed buy order for 0.001 BTC/USDT at 50000 with stop loss at 49500.0 and take profit at 51000.0
.2024-06-08 14:52:54,697 - INFO - Time synchronized with time.google.com. Offset: 270.06887793540955 seconds
F
======================================================================
FAIL: test_synchronize_time (__main__.TestTradingFunctions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\unittest\mock.py", line 1379, in patched
    return func(*newargs, **newkeywargs)
  File "f:\trading\latest + 4 pdf combined\test_trading_bot.py", line 24, in test_synchronize_time
    self.assertEqual(time_offset, 0.123)
AssertionError: 270.06887793540955 != 0.123

----------------------------------------------------------------------
Ran 3 tests in 0.134s

FAILED (failures=1)


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/tempCodeRunnerFile
.py"

PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/Technical_Indicato
rs.py"

2024-06-08 14:53:14,771 - INFO - Time synchronized with time.google.com. Offset: 270.0655872821808 seconds
2024-06-08 14:53:14,771 - INFO - Time synchronized with offset: 270
2024-06-08 14:53:14,781 - INFO - Initialized Bybit exchange
2024-06-08 14:53:15,087 - ERROR - Error fetching OHLCV data: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window
param. req_timestamp[1717838594781],server_timestamp[1717838865116],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838865116}
2024-06-08 14:53:15,087 - ERROR - An error occurred during the main execution: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timesta
mp or recv_window param. req_timestamp[1717838594781],server_timestamp[1717838865116],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838865116}


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/synchronize_exchan
ge_time.py"

2024-06-08 14:53:20,233 - INFO - Time synchronized with time.google.com. Offset: 270.0712842941284 seconds
Time offset: 270.0712842941284 seconds


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/Risk Management.py

"
2024-06-08 14:53:26,483 - INFO - System time synchronized: 2024-06-08 14:57:56.526182
2024-06-08 14:53:26,492 - INFO - Initialized Bybit exchange
2024-06-08 14:53:26,828 - ERROR - Failed to fetch historical data: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_w
indow param. req_timestamp[1717838606493],server_timestamp[1717838876843],recv_window[10000]","result":{},"retExtInfo":{},"time":1717838876843}
Traceback (most recent call last):
  File "f:\trading\latest + 4 pdf combined\Risk Management.py", line 146, in <module>
    main()
  File "f:\trading\latest + 4 pdf combined\Risk Management.py", line 137, in main
    data = fetch_historical_data(exchange, symbol)
  File "f:\trading\latest + 4 pdf combined\Risk Management.py", line 52, in fetch_historical_data
    raise e
  File "f:\trading\latest + 4 pdf combined\Risk Management.py", line 45, in fetch_historical_data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\bybit.py", line 2178, in fetch_ohlcv
    self.load_markets()
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\exchange.py", line 1539, in load_markets
    currencies = self.fetch_currencies()
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\bybit.py", line 1303, in fetch_currencies
    response = self.privateGetV5AssetCoinQueryInfo(params)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\types.py", line 35, in unbound_method
    return _self.request(self.path, self.api, self.method, params, config=self.config)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\exchange.py", line 3740, in request
    return self.fetch2(path, api, method, params, headers, body, config)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\exchange.py", line 3737, in fetch2
    return self.fetch(request['url'], request['method'], request['headers'], request['body'])
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\exchange.py", line 695, in fetch
    self.handle_errors(http_status_code, http_status_text, url, method, headers, http_response, json_response, request_headers, request_body)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\bybit.py", line 8156, in handle_errors
    self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ccxt\base\exchange.py", line 4122, in throw_exactly_matched_exception
    raise exact[string](message)
ccxt.base.errors.InvalidNonce: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window param. req_timestamp[171783860
6493],server_timestamp[1717838876843],recv_window[10000]","result":{},"retExtInfo":{},"time":1717838876843}


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/Placing Orders.py"

2024-06-08 14:53:32,820 - INFO - Initialized Bybit exchange
Traceback (most recent call last):
  File "f:\trading\latest + 4 pdf combined\Placing Orders.py", line 180, in <module>
    main()
  File "f:\trading\latest + 4 pdf combined\Placing Orders.py", line 168, in main
    time_offset = synchronize_exchange_time(exchange)
  File "f:\trading\latest + 4 pdf combined\Placing Orders.py", line 28, in synchronize_exchange_time
    time_offset = synchronize_time(exchange)
  File "f:\trading\latest + 4 pdf combined\synchronize_exchange_time.py", line 11, in synchronize_time
    response = client.request(ntp_server)
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\site-packages\ntplib.py", line 296, in request
    addrinfo = socket.getaddrinfo(host, port)[0]
  File "C:\Users\rajes\AppData\Local\Programs\Python\Python310\lib\socket.py", line 955, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
TypeError: getaddrinfo() argument 1 must be string or None


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/fetch_data.py"

2024-06-08 14:53:40,181 - INFO - Time synchronized with exchange. Offset: 0 milliseconds
2024-06-08 14:53:40,593 - ERROR - An error occurred while fetching data: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or
recv_window param. req_timestamp[1717838620181],server_timestamp[1717838890615],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838890615}
2024-06-08 14:53:40,593 - ERROR - A network error occurred: bybit {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window p
aram. req_timestamp[1717838620181],server_timestamp[1717838890615],recv_window[5000]","result":{},"retExtInfo":{},"time":1717838890615}


PS F:\trading\latest + 4 pdf combined> & C:/Users/rajes/AppData/Local/Programs/Python/Python310/python.exe "f:/trading/latest + 4 pdf combined/Backtesting.py"

Traceback (most recent call last):
  File "f:\trading\latest + 4 pdf combined\Backtesting.py", line 24, in <module>
    time_offset = synchronize_time(exchange, 'pool.ntp.org')
  File "f:\trading\latest + 4 pdf combined\synchronize_exchange_time.py", line 9, in synchronize_time
    while retries < max_retries:
TypeError: '<' not supported between instances of 'int' and 'str'


