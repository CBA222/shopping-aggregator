"""
This file stores definitions for all store readers
It allows the main config file to access them without directly
import the individual python modules
"""

from readers.bestbuy import BestBuyReader
from readers.walmart import WalmartReader

PATH = ""

READERS = {
    "bestbuy": BestBuyReader,
    "walmart": WalmartReader,
}