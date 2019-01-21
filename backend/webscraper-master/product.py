import persistent, persistent.list
import json

class Product(persistent.Persistent):
    """
    Class representing a single, unique product

    name: name of product
    description: description of product
    image: image url of product
    listings: list of Listing objects pertaining to the product
    """

    def __init__(self, name, description = None, image = None, model_number = None, upc = None):
        self.name = name
        self.description = description
        self.image = image
        self.model_number = model_number
        self.upc = upc
        self.listings = persistent.list.PersistentList()

    def add_listing_param(self, vendor, price, url):
        self.listings.append(Listing(vendor, price, url))

    def add_listing(self, listing):
        self.listings.append(listing)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if self.model_number != None and other.model_number != None:
            return self.model_number == other.model_number
        elif self.upc != None and other.upc != None:
            return self.upc == other.upc
        else:
            return self.name == other.name
        
class Listing(persistent.Persistent):
    """
    Class representing one listing of a specific product

    vendor: Vendor selling the product
    price: current price of product at the vendor
    url: url to the listing page
    """

    def __init__(self, vendor, price, url):
        self.vendor = vendor
        self.price = price
        self.url = url

    def __str__(self):
        return self.vendor + " " + self.price


# Prepare products for inserting into Django database
def prepare_products(product_list):
    key = 1
    json_list = []
    for product in product_list:
        dict =  {
            "model": "shop.Product",
            "pk": key,
            "fields": {
                "name": product.name,
                "price": product.listings[0].price, #temp to get rid of $ sign
                "url": product.listings[0].url,
                "image_url": product.image
            }
        }
        json_list.append(dict)
        key += 1
    return json_list