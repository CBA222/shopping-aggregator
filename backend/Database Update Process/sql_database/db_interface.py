from sqlalchemy import create_engine, or_
from sqlalchemy.sql import select, text
import json
from .create_db import products

class DatabaseInterface:
    """
    This class is responsible for actually interfacing with the raw database
    It has functions for inserting products into the database
    Store readers will not call these functions directly but rather a DatabaseUpdater
    will call it.
    """

    def __init__(self, conn):
        self.conn = conn
        self.name=''
        
    def add_listing(
        self, 
        product_name, 
        product_image_urls, 
        product_thumbnail,
        product_description,
        product_upc, 
        product_model_number,
        listing_vendor, 
        listing_price, 
        listing_url):

        existing = self.conn.execute(
            select([products]).where(or_(products.c.upc==product_upc, products.c.model_number==product_model_number))
        ).fetchone()

        if existing is not None:
            self.conn.execute(
                products.update().where(products.c.id==existing['id']),
                name = product_name if existing['name'] == None else existing['name'],
                image_urls = product_image_urls if existing['image_urls'] == None else existing['image_urls'],
                thumbnail = product_thumbnail if existing['thumbnail'] == None else existing['thumbnail'],
                description = product_description if existing['description'] == None else existing['description'],
                listings=existing['listings'] + [{'vendor':listing_vendor, 'price':listing_price, 'url':listing_url}]
            )
        else:
            self.conn.execute(
                products.insert(),
                name=product_name,
                image_urls=product_image_urls,
                thumbnail=product_thumbnail,
                description=product_description,
                upc=product_upc,
                model_number=product_model_number,
                listings=[{'vendor':listing_vendor, 'price':listing_price, 'url':listing_url}]
            )

    def export_to_fixtures(self, output_path):
        raw_data = self.conn.execute(
            products.select()
        )

        json_list = []
        for row in raw_data:
            listings = row['listings']
            lowest = listings[0]
            for l in listings:
                if l['price'] < lowest['price']:
                    lowest = l

            temp =  {
                "model": "shop.Product",
                "pk": None,
                "fields": {
                    "name": row[1],
                    "image_url": row[2][0],
                    "description": row[3],
                    "upc": row[4],
                    "model_number": row[5],
                    "best_vendor": lowest['vendor'],
                    "best_price": lowest['price'],
                    "best_url": lowest['url'],
                    "listings": listings
                }
            }
            json_list.append(temp)
        
        with open(output_path, 'w') as outfile:
            json.dump(json_list, outfile)

"""
if __name__ == '__main__':
    #engine = create_engine('postgresql://postgres:lego_10010@localhost/product_database_1')
    #conn = engine.connect()

    #db = DatabaseInterface('postgresql://postgres:lego_10010@localhost/product_database_1')
    #db.add_listing('Sony IMAX Camera',['image1.png'],'description','1827398172391','YYY66TR','BestBuy','1499.99','bestbuy.com')

    db = DatabaseInterface('postgresql://postgres:lego_10010@localhost/product_database_2')
    db.add_listing('Sony IMAX Camera',['image1.png'], 'thumb.png', 'description','1827398172391','YYY66TR','Wal-Mart','1599.99','walmart.com')
"""