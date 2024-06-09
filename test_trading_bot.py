import unittest
from unittest.mock import MagicMock, patch
import ccxt
from tradingbot import initialize_exchange, synchronize_time, place_order_with_risk_management

class TestTradingFunctions(unittest.TestCase):

    def setUp(self):
        self.api_key = 'test_api_key'
        self.api_secret = 'test_api_secret'
        self.exchange = ccxt.bybit({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,
        })

    def test_initialize_exchange(self):
        exchange = initialize_exchange(self.api_key, self.api_secret)
        self.assertIsInstance(exchange, ccxt.bybit)

    @patch('tradingbot.synchronize_time', return_value=0.123)
    def test_synchronize_time(self, mock_synchronize_time):
        time_offset = synchronize_time()
        self.assertEqual(time_offset, 0.123)

    def test_place_order_with_risk_management(self):
        self.exchange.create_order = MagicMock(return_value={'price': 50000})
        
        place_order_with_risk_management(self.exchange, 'BTC/USDT', 'buy', 0.001, 0.01, 0.02)
        self.exchange.create_order.assert_any_call('BTC/USDT', 'market', 'buy', 0.001)
        self.exchange.create_order.assert_any_call('BTC/USDT', 'stop', 'sell', 0.001, 49500.0)
        self.exchange.create_order.assert_any_call('BTC/USDT', 'limit', 'sell', 0.001, 51000.0)

if __name__ == '__main__':
    unittest.main()
