import pytest
from scripts.WalletManagement import get_balances, rebalance_wallets, get_total_balance, make_trades, close_trades, make_transfer
from brownie import GNSTradingV6_2, config, accounts, Contract, GNSDaiTokenV5
import time
from scripts.Bot import Positions, PositionOptions, BuyOptions



trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
gfarm_dai = "0x04B2A6E51272c82932ecaB31A5Ab5aC32AE168C3"

account1 = accounts.add(config["wallets"]["wallet1"])
account2 = accounts.add(config["wallets"]["wallet2"])
account3 = accounts.add(config["wallets"]["wallet3"])
account4 = accounts.add(config["wallets"]["wallet4"])

BTC_price = 20592.20

our_accounts = [account1, account2, account3, account4]

referrer = "0x786e22B4BF1ef3a73Be33dF36E61321CCddba345"


# Tests won't run because the GNSTrading contract is defined outside of a function in WalletManagement.py

def test_rebalance_wallets():
    rebalance_wallets()
    make_transfer(account2, account1, 5000*10**18)
    balances = get_balances()
    assert balances[1]== balances[0]+10000 
    rebalance_wallets()
    balances = get_balances()
    assert balances[1] == balances[0]

def test_make_trades():
    last_position = Positions(True, BTC_price , get_total_balance())
    make_trades(last_position, 0, BTC_price, True, 5, 25, 25, 0.25, referrer)
    assert get_total_balance() < last_position.tvl_at_open

def test_close_trades():
    last_position = Positions(True, BTC_price , get_total_balance())
    close_trades(last_position, 0, BTC_price)
    assert get_total_balance() > last_position.tvl_at_open
