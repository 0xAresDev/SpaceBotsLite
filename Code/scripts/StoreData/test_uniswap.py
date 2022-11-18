from uniswap import Uniswap
from UniswapData import *
import pytest


# might fail in the future, hopefully we all will be happy about that!
def test_get_price():
    price = get_uniswap_price()
    assert price < 100000 and price > 10000