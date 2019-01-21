import ZODB, ZODB.FileStorage
import BTrees, BTrees.OOBTree
import transaction
import json

class ProductDatabase:

    def __init__(self, path):
        storage = ZODB.FileStorage.FileStorage(path)
        db = ZODB.DB(storage)
        conn = db.open()
        self.root = conn.root()

    def create_database(self):
        self.root.products = BTrees.OOBTree.BTree()
        transaction.commit()

    """
    def add_listing(self, product, listing):
        if product.name not in self.root.products.keys():
            product.add_listing(listing)
            self.root.products.update( [ (product.name, product) ] )
        else:
            self.root.products[product.name].add_listing(listing)
        transaction.commit()
    """

    def add_listing(self, product, listing):
        if not any(product == p for p in self.root.products.values()):
            product.add_listing(listing)
            self.root.products.update( [ (product.name, product) ] )
        else:
            self.root.products[product.name].add_listing(listing)
        transaction.commit()

    def export_to_json(self, output_path):
        json_list = []
        for product in self.root.products.values():
            dict =  {
                "model": "shop.Product",
                "pk": None,
                "fields": {
                    "name": product.name,
                    "description": product.description,
                    "upc": product.upc,
                    "model_number": product.model_number,
                    "image_url": product.image,
                    "price": product.listings[0].price, 
                    "url": product.listings[0].url,
                }
            }
            json_list.append(dict)
        
        with open(output_path, 'w') as outfile:
            json.dump(json_list, outfile)