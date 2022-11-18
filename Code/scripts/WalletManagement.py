from mimetypes import init
from turtle import position
from brownie import GNSTradingV6_2, config, accounts, Contract, GNSDaiTokenV5
import time
from .Interaction import open_trade, close_trade
from .Variables import *


"""
Gains Trade only allows 3 positions per Wallet and Traiding pair. We DCA and therefore need at least 11 positions.
The solution for this problem is this file. We use 4 wallets instead of one. Everything happens automatically.
"""


# Account config
account1 = accounts.add(config["wallets"]["wallet1"])
account2 = accounts.add(config["wallets"]["wallet2"])
account3 = accounts.add(config["wallets"]["wallet3"])
account4 = accounts.add(config["wallets"]["wallet4"])

our_accounts = [account1, account2, account3, account4]


percent_fall_to_account = {
    0: account1,
    1: account1,
    2: account1,
    3: account2,
    4: account2,
    5: account2,
    6: account3,
    7: account3,
    8: account3,
    9: account4,
    10: account4
}

# for simulation purposes
all_trades = []



# approves DAI for all wallets
def approve_all(amount):
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    for a in our_accounts:
        gnsDaiTokenV5.approve(trading_v6_testnet, amount, {"from": a})

# gets some testnet dai for each wallet
def get_testnet_dai():
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    for a in our_accounts:
        gnsDaiTokenV5.getFreeDai({"from": a})


# returns balance of all wallets combined
def get_total_balance():
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    if not simulate:
        total_balance = 0
        for a in our_accounts:
            total_balance += gnsDaiTokenV5.balanceOf(a)
    else:
        total_balance = 10000
    return total_balance/10**18


# returns balances for each wallet
def get_balances():
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    return [gnsDaiTokenV5.balanceOf(a)/10**18 for a in our_accounts]


# rebalances all wallets to have the same amount of DAI
def rebalance_wallets():
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    balances = get_balances()
    total_balace = 0
    for b in balances:
        total_balace += b
    
    for i, a in enumerate(our_accounts[1:]):
        if balances[i+1]> 0:
            tx = gnsDaiTokenV5.transfer(account1, balances[i+1]*10**18, {"from": a})
            tx.wait(1)
    for a in our_accounts[1:]:
        tx = gnsDaiTokenV5.transfer(a, total_balace/4 * 10**18, {"from": account1})
        tx.wait(1)
    print("Succesfully rebalanced wallets!")

# makes a trade 
def make_trades(last_position, pairIndex, price, buy_trade, leverage, take_profit, stop_loss, slippage, referrer):
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    if last_position.percent_fall == 0:
        position_size = last_position.tvl_at_open*0.1
    else:
        position_size = last_position.tvl_at_open*0.05
    
    percent_fall = last_position.percent_fall
    account = percent_fall_to_account[percent_fall]
    
    if not simulate:
        open_trade(account, pairIndex, price, position_size, buy_trade, leverage, take_profit, stop_loss, slippage, referrer)
    else:
        long = "Long"
        if not buy_trade:
            long = "Short"
        initial = "Initial"
        if last_position.percent_fall != 0:
            initial = "DCA"
        print(f"Open {long}, {initial} {last_position.percent_fall} {price}")
        all_trades.append([0, long, initial, price])

# Closes trades
def close_trades(last_position, pairIndex, price):
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    percent_fall = last_position.percent_fall
    if not simulate:
        for i in range(last_position.percent_fall+1):
            close_trade(percent_fall_to_account[percent_fall], pairIndex, percent_fall%3)
        rebalance_wallets()
    else:
        print(f"Close all positions at {price}")
        all_trades.append([1, price])

# just a simple DAI transfer between 2 wallets
def make_transfer(to, from_, amount):
    gnsDaiTokenV5 = GNSDaiTokenV5.at(gfarm_dai)
    tx = gnsDaiTokenV5.transfer(to, amount, {"from": from_})
    tx.wait(1)


# only for simulation purposes
# Trade: Open: [0, long/short, initial/DCA, price]
#        Short:[1, price]
def get_all_trades():
    return all_trades


def main():
    pass