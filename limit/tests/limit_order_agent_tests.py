import unittest
import sys
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client_mock = ExecutionClient
        self.limit_order_agent = LimitOrderAgent(self.execution_client_mock)

    def test_add_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 99.5)
        self.limit_order_agent.add_order('buy', 'TATA', 10000, 101)
        self.limit_order_agent.add_order('buy', "AAPL", 200, 120)

        self.assertEqual(self.limit_order_agent.orders[0], ('buy', "IBM", 1000, 99.5))
        self.assertEqual(self.limit_order_agent.orders[1], ('buy', 'TATA', 10000, 101))
        self.assertEqual(self.limit_order_agent.orders[2], ("buy", "AAPL", 200, 120))
        self.assertEqual(len(self.limit_order_agent.orders), 3)
        print("test_add_order Passed Successfully")

    def test_execute_buy_order(self):
        self.limit_order_agent.add_order('buy', 'IBM', 1000, 100.5)
        self.limit_order_agent.on_price_tick('IBM', 99.0)
        self.limit_order_agent.add_order('buy', 'TATA', 10000, 200) # limit for tata is 200
        self.limit_order_agent.on_price_tick('TATA', 201)
        self.assertEqual(len(self.limit_order_agent.orders),2)
        print("test_execute_buy_order Passed Successfully")

    def test_execute_sell_order(self):
        self.limit_order_agent.add_order('sell', 'IBM', 1000, 101.0)
        self.limit_order_agent.on_price_tick('IBM', 102.0)
        self.limit_order_agent.add_order('sell', 'TATA', 10000, 200)
        self.limit_order_agent.on_price_tick('TATA', 201)
        self.assertFalse(self.limit_order_agent.orders)
        print("test_execute_sell_order Passed Successfully")

    def test_execute_wrong_order(self):
        self.limit_order_agent.add_order('wrong', 'IBM', 1000, 101.0)
        self.limit_order_agent.on_price_tick('IBM', 102.0)
        self.assertEqual(len(self.limit_order_agent.orders),0)
        print("test_execute_sell_order Passed Successfully")


if __name__ == '__main__':
    unittest.main()
