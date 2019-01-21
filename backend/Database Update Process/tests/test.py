from sql_database.db_updater import DatabaseUpdater
from sql_database.db_interface import DatabaseInterface

from readers.bestbuy import BestBuyReader
from readers.walmart import WalmartReader

db_interface = DatabaseInterface('postgresql://postgres:lego_10010@localhost/product_database_2')

my_readers = [
    WalmartReader('rj9w6a59zbyckgdn4e7e9rqz', 3),
    BestBuyReader('Xsk22axb3WQ4bA3KCUbuA3Qf', 5)
]

db_updater = DatabaseUpdater(db_interface, my_readers)
db_updater.update_all(True)