from sqlalchemy import create_engine, or_
from sqlalchemy.sql import select, text

from .create_db import products
store_cache = ''

from search_interface import SearchInterface

class UpdateInterface:
    """
    This class updates the product database and the search index from
    a list of products
    """

    def __init__(self, conn, search_path, index_name):
        self.conn = conn
        self.search_interface = SearchInterface(search_path, index_name)

    def retrieve_store(self, name):
        return self.conn.execute(
            select([store_cache]).where(store_cache.c.name==name)
        ).fetchone()

    def add_store_listings(self, store, product_list):
        """
        This function takes a list of products 
        """

        existing_products = self.retrieve_store(store)
        search_index_update = []
        
        for product in product_list:

            # Check if product already exists in database
            existing = self.conn.execute(
                select([products]).where(or_(products.c.upc==product['upc'], products.c.model_number==product['model_number']))
            ).fetchone()

            # If the product exists in the database
            if existing is not None:
                # if vendor listing already in product data, update vendor listing
                if len([x for x in existing['listings'] if x['vendor'] == store]) > 0:

                    new_listings = existing['listings']
                    new_listings[store]['price'] = product['listing_price']
                    new_listings[store]['url'] = product['listing_url']

                    self.conn.execute(
                        products.update().where(products.c.id==existing['id']),
                        listings=new_listings
                    )
                # if vendor listing not in product data, create new vendor listing
                else:
                    self.conn.execute(
                        listings=existing['listings'] + \
                        [{'vendor': product['listing_vendor'], 'price': product['listing_price'], 'url': product['listing_url']}]
                    )
            # If the product does not exist, create new listing in database and search index
            else:
                self.conn.execute(
                    products.insert(),
                    name=product['name'],
                    image_urls=product['image_urls'],
                    thumbnail=product['thumbnail'],
                    description=product['description'],
                    upc=product['upc'],
                    model_number=product['model_number'],
                    listings=[{'vendor': product['vendor'], 'price': product['price'], 'url': product['url']}]
                )

                search_index_update.append({
                    'type': 'create',
                    'data': {
                        'name': product['name'],
                        'description': product['description'],
                        'upc': product['upc'],
                        'model_number': product['model_number']
                    }
                })

        # clean up product listings that should not exist any longer

        new_products = [product['upc'] for product in product_list]
        missing_products = set(existing_products) - set(new_products)

        for upc in missing_products:
            old_listings = self.conn.execute(
                products.select().where(products.c.upc==upc)
            ).fetchone()['listings']

            new_listings = [x for x in old_listings if x['vendor'] != store]

            self.conn.execute(
                products.update().where(products.c.upc==upc),
                listings=new_listings
            )

            search_index_update.append({
                'type': 'delete',
                'upc': product['upc'],
            })

        self.search_interface.update_index(search_index_update)