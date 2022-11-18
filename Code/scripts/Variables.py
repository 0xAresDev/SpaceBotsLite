# gains trade contract
trading_v6_testnet = "0x81465dF3c64B18b4092990eB73200A3814AF75E5"
# DAI token contract
gfarm_dai = "0x04B2A6E51272c82932ecaB31A5Ab5aC32AE168C3"
# gains trade referral wallet to use
referral_wallet=""
# Index of the trading pair, can be found in the gains trade docs
pairIndex = 0
# leverage that should be used
leverage = 5
# Take profit isn't implemented yet
take_profit = 0
# stop loss is implemented in %
stop_loss = 15
# max allowed slippage for your trade
slippage = 0.25



# For simulation purposes
"""
Simulate has 2 options. hourly=True means that the simulation will use Bitstamps hourly data. We have a few years worth of data here
hourly=False will use binace minutely data, we only have a couple of month worth of data. All from 2022
"""
simulate = True
hourly = False
# Defines what's the min time period between each buy for simulations, cant be changed for the actual bot yet
iterations_since_last_investment = 10