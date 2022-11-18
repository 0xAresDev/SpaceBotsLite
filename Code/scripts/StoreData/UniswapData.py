import requests
import json


# returns BTC price data from crypto compare
def get_uniswap_price():
    response_API = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json["USD"]

