from walmart import WalmartReader
from sql_database.db_interface import DatabaseInterface

reader = WalmartReader('rj9w6a59zbyckgdn4e7e9rqz')
product_list = reader.read_entire_category('3944')
#product_list = reader.read_category('5438')

db = DatabaseInterface('postgresql://postgres:lego_10010@localhost/product_database_1')

for p in product_list:
    db.add_listing_from_objects(p[0], p[1])