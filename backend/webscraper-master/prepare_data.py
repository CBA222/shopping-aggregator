from ebay import EbayReader
from product_database import ProductDatabase
from product import prepare_products

if __name__ == '__main__':
    appid = 'BrianLin-fullshel-PRD-f7141958a-eee81537'
    reader = EbayReader(appid)
    product_list = reader.get_products_by_category(293, 1000)

    path = '/Users/apple/Desktop/Projects/ebaydb/ebaydb.fs'
    db = ProductDatabase(path)
    db.create_database()

    for p in product_list:
        db.add_listing(p[0], p[1])