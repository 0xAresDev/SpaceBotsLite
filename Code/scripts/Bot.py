import talib
import numpy as np
from enum import Enum
import datetime
from .WalletManagement import make_trades, close_trades, rebalance_wallets, get_total_balance, get_all_trades
from .StoreData.main import read_data_from_db, eth, dai
from .StoreData.UniswapData import get_uniswap_price
import sched, time
import pandas as pd
import warnings
from .StoreData.bitstamp_BTCUSD_1h import getBTC1h
from .StoreData.binanceBTCUSD import getBTC1m
warnings.simplefilter(action='ignore', category=Warning)
import logging
logging.disable(logging.WARNING)
logging.disable(logging.INFO)
import pathlib, os
from .Variables import *


class PositionOptions(Enum):
    OPEN_LONG = 1
    CLOSE_LONG = 2
    OPEN_SHORT = 3
    CLOSE_SHORT = 4

class BuyOptions(Enum):
    INITIAL = 1
    DCA = 2


class Positions:
    
    def __init__(self, isLong, price, tvl_at_open, percent_fall=0):
        self.isLong = isLong
        self.price = price
        self.percent_fall = percent_fall
        self.tvl_at_open = tvl_at_open

    def longPosition(data):
        # implement math here if long positions should be opened, should return OPEN_LONG or CLOSE_LONG
        pass
        
    def shortPosition(data):
        # implement math here if short positions should be opened, should return OPEN_SHORT or CLOSE_SHORT
        pass
    

positions = []
referrer = referral_wallet
last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)


def bot(data, price):
    global last_buy, positions, iterations_since_last_investment, hourly
    
    """
    Your data prep belongs here
    """
    
    price = price
    long = Positions.longPosition(data)
    short = Positions.shortPosition(data)


    # time calculations so last investment > 10 mins ago
    now = datetime.datetime.now()
    time_difference = (now - last_buy).total_seconds()
    iterations_since_last_investment += 1

    # if we don't have any positions open yet
    if len(positions) == 0:
        if long == PositionOptions.OPEN_LONG:
            # open long position
            position = Positions(True, price, get_total_balance(), 0)
            positions.append(position)
            make_trades(position, pairIndex, price, True, leverage, take_profit, stop_loss, slippage, referrer)
            last_buy = datetime.datetime.now()
            iterations_since_last_investment = 0
        else:
            if short == PositionOptions.OPEN_SHORT:
                # open short position
                position = Positions(False, price, get_total_balance(), 0)
                positions.append(position)
                make_trades(position, pairIndex, price, False, leverage, take_profit, stop_loss, slippage, referrer)
                last_buy = datetime.datetime.now()
                iterations_since_last_investment = 0

    
    # if we have already multiple positions opened
    else:
        # price difference for DCA part
        price_difference = price - positions[0].price

        isLong = positions[0].isLong
        if isLong:
            # Stop loss, Stop loss gets done automatically by Gains Trade. Howesver we need to delete the positions.
            s_l = False
            if price_difference < -1 * positions[0].price * 0.15:
                s_l = True

            # Close when market gets too bearish
            if long == PositionOptions.CLOSE_LONG or s_l:
                last_position = positions[-1]
                close_trades(last_position, pairIndex, price)
                last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)
                iterations_since_last_investment = 10
                positions = []
            
            # DCA part
            elif long == PositionOptions.OPEN_LONG and (time_difference>60*10 or ((simulate and hourly) or (not hourly and iterations_since_last_investment >= 10 and simulate))): # check if price moved in wrong direction
                if price_difference < -1 * positions[0].price * (positions[-1].percent_fall+1)/100 and positions[-1].percent_fall < 10:
                    # DCA, open another position
                    position = Positions(True, price, positions[0].tvl_at_open, positions[-1].percent_fall+1)
                    positions.append(position)
                    make_trades(position, pairIndex, price, True, leverage, take_profit, stop_loss, slippage, referrer)
                    last_buy = datetime.datetime.now()
                    iterations_since_last_investment = 0


        else:

            # Stop loss
            s_l = False
            if price_difference > positions[0].price * 0.15:
                s_l = True

            #Close when markets get too bulish
            if short == PositionOptions.CLOSE_SHORT or s_l:
                last_position = positions[-1]
                close_trades(last_position, pairIndex, price)
                last_buy = datetime.datetime.now()-datetime.timedelta(minutes=15)
                iterations_since_last_investment = 10
                positions = []

            # DCA part
            elif short == PositionOptions.OPEN_SHORT and (time_difference>60*10 or ((simulate and hourly) or (not hourly and iterations_since_last_investment >= 10 and simulate))):
                if price_difference > positions[0].price * (positions[-1].percent_fall+1)/100 and positions[-1].percent_fall < 10:
                    # DCA, open another position
                    position = Positions(False, price, positions[0].tvl_at_open, positions[-1].percent_fall+1)
                    positions.append(position)
                    make_trades(position, pairIndex, price, False, leverage, take_profit, stop_loss, slippage, referrer)
                    last_buy = datetime.datetime.now()
                    iterations_since_last_investment = 0
            
    

def main():
    
    # simulations with bitstamp hourly data
    if simulate and hourly:
        # simulation part, go through time
        directory = pathlib.Path(__file__).parent.resolve()
        data = getBTC1h('2022-01-01','2022-09-31', filename=os.path.join(directory, 'StoreData/Bitstamp_BTCUSD_1h.csv'))
        data_indicator = data[data.index % 24 == 0]  # Selects every 3rd raw starting from 0
        data_indicator["Close"] = data_indicator["Close"].astype("double")
        data_indicator = data_indicator.reset_index()

        for index, row in data_indicator.iterrows():
            if index > 15:
                data_indicator_current = data_indicator.copy(deep=True)
                data_indicator_current = data_indicator_current.iloc[index-14:index+1]
                for i in range(24):
                    if index*24+i+1 < data.shape[0]:
                        price = data[index*24+i:index*24+i+1]["Close"]
                        bot(data_indicator_current, float(price))
        
        
        # calculate results of bot
        # Trade: Open: [0, long/short, initial/DCA, price]
        #        Short:[1, price]
        trades = get_all_trades()
        value = 10000
        value_at_first_buy = 10000
        trades_per_position = []

        for trade in trades:
            if trade[0] == 0:
                long = 1
                if trade[1] == "Long":
                    long = 0

                if trade[2] == "Initial":
                    trades_per_position.append([long, value*0.1, trade[3]])
                    value = value * 0.9
                else:
                    trades_per_position.append([long, value_at_first_buy*0.05, trade[3]])
                    value = value - value_at_first_buy*0.05
            else:
                price_now = trade[1]
                v = 0
                if trades_per_position[0][0] == 0:
                    for t in trades_per_position:
                        v += t[1] + (price_now - t[2]) * t[1]/t[2] * leverage
                else:
                    for t in trades_per_position:
                        v += t[1] + (t[2]-price_now) * t[1]/t[2] * leverage

                value += v
                value_at_first_buy = value
                trades_per_position = []
                print(value)
                

    # Simulation with binance data
    elif simulate and hourly == False:
        directory = pathlib.Path(__file__).parent.resolve()
        data = getBTC1m(filename_base=os.path.join(directory, 'StoreData/BTCBUSD-1m-2022-00.csv'))
        data_indicator = data[data.index % (24*60) == 0]  # Selects every 3rd raw starting from 0
        data_indicator["Close"] = data_indicator["Close"].astype("double")
        data_indicator = data_indicator.reset_index()
        for index, row in data_indicator.iterrows():
            if index > 15:
                data_indicator_current = data_indicator.copy(deep=True)
                data_indicator_current = data_indicator_current.iloc[index-14:index+1]

                for i in range(24*60):
                    if index*24*60+i+1 < data.shape[0]:
                        price = data[index*24*60+i:index*24*60+i+1]["Close"]
                        bot(data_indicator_current, float(price))
        
        # Calculate the results    
        # Trade: Open: [0, long/short, initial/DCA, price]
        #        Short:[1, price]
        trades = get_all_trades()
        value = 10000
        value_at_first_buy = 10000
        # [market direction, amount, price]    
        trades_per_position = []

        for trade in trades:
            if trade[0] == 0:
                long = 1
                if trade[1] == "Long":
                    long = 0

                if trade[2] == "Initial":
                    trades_per_position.append([long, value*0.1, trade[3]])
                    value = value * 0.9
                else:
                    trades_per_position.append([long, value_at_first_buy*0.05, trade[3]])
                    value = value - value_at_first_buy*0.05
            else:
                price_now = trade[1]
                v = 0
                if trades_per_position[0][0] == 0:
                    for t in trades_per_position:
                        v += t[1] + (price_now - t[2]) * t[1]/t[2] * leverage
                else:
                    for t in trades_per_position:
                        v += t[1] + (t[2]-price_now) * t[1]/t[2] * leverage

                value += v
                value_at_first_buy = value
                trades_per_position = []
                print(value)
        print(len(trades))

    else:
        # Here is the actual real world trading
        # Does all the calculations every minute
        s = sched.scheduler(time.time, time.sleep)

        def main_func(sc):
            
            data = read_data_from_db(15)
            data.reverse()
            data = pd.DataFrame(data, columns=["Close", "Time"])
            price = get_uniswap_price(eth, dai)
            bot(data, price)
        
            sc.enter(60, 1, main_func, (sc,))

        s.enter(60, 1, main_func, (s,))
        s.run()
        
