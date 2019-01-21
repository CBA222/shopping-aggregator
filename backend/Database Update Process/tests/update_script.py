from readers.bestbuy import BestBuyReader
from readers.walmart import WalmartReader
from sql_database.db_interface import DatabaseInterface
from sql_database.db_updater import DatabaseUpdater

path = ''
my_interface = DatabaseInterface(path)

my_readers = [
    WalmartReader('key', 3),
    BestBuyReader('key', 5)
]

my_updater = DatabaseUpdater(my_interface, my_readers)

for r in my_readers:
    r.set_logger(my_updater)

my_updater.update_all()