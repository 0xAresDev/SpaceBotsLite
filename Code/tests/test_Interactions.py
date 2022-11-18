import pytest
from scripts.Interaction import open_trade, close_trade
from brownie import GNSTradingV6_2, config, accounts, Contract
import time


trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
my_account = "0xc0Ea5c77570efDD46911436bdb295cAc57720a31"
account1 = accounts.add(config["wallets"]["wallet1"])
BTC_price = 20621.73

def test_open_and_close_trade():
    # Test for BTC/DAI
    #account, pairIndex, price, position_size, buy_trade, leverage, take_profit, stop_loss, slippage, referrer=my_account
    events = open_trade(account1, 0, BTC_price, 1000, True, 10, 25, 10, 3, my_account)
    assert "MarketOrderInitiated" in events.keys() 
    time.sleep(10)
    events = close_trade(account1, 0, 0)
    assert "MarketOrderInitiated" in events.keys() 


