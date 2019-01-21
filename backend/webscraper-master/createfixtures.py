import ZODB, ZODB.FileStorage
from product import prepare_products
import json

def create_fixtures(db_path, out_path):
    storage = ZODB.FileStorage.FileStorage(db_path)
    db = ZODB.DB(storage)
    conn = db.open()
    root = conn.root()

    jsonlist = prepare_products(list(root.products.values()))

    with open(out_path, 'w') as outfile:
        json.dump(jsonlist, outfile)