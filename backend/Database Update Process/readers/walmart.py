import requests
import sys
import json

#from .product import Product, Listing
from .storereader import StoreReader

def traverse(data):
    if 'children' not in data.keys():
        return [data['id']]

    id_list = []
    for child in data['children']:
        id_list += traverse(child)
    
    return id_list

def get_categories(self):
    path = '/Users/apple/Desktop/Projects/webscraper-master/walmart_categories.json'
    data = {}
    with open(path) as file:
        data = json.load(file)
    data = data['categories']
    id_list = []
    for d in data:
        id_list += traverse(d)
    return id_list

class WalmartReader(StoreReader):

    def __init__(self, apikey, page_limit):
        self.apikey = apikey
        self.vendor = "Wal-Mart"
        self.page_limit = page_limit

        path = '/Users/apple/Desktop/Projects/webscraper-master/walmart_categories.json'
        with open(path) as file:
            data = json.load(file)
        data = data['categories']
        self.category_tree = {}
        for c in data:
            self.category_tree[c['id']] = c

    def read_all(self):
        product_list = []
        for c in self.category_tree:
            product_list += self.recursive_read(c)
        return product_list

    def read_test(self):
        return self.read_entire_category('3944')

    def read_entire_category(self, category_id):
        try:
            return self.recursive_read(self.category_tree[category_id])
        except IndexError:
            pass

    def recursive_read(self, tree):
        if 'children' not in tree.keys():
            return self.read_category(tree['id'], self.page_limit) #page limit

        product_list = []
        for child in tree['children']:
            product_list += self.recursive_read(child)

        return product_list
    
    def read_category(self, category_id, count=3):
        product_list = []

        response = requests.get(
            'http://api.walmartlabs.com/v1/paginated/items',
            params={
                'format': 'json',
                'category': category_id,
                'apiKey': self.apikey,
            }
        )

        iter = 0
        try:
            response.json()
        except json.decoder.JSONDecodeError:
            return []
        while 'items' in response.json().keys():
            for item in response.json()['items']:
                try:
                    product_list.append(
                        [
                            {
                                'name': item['name'],
                                'description': item['longDescription'],
                                'model_number': item['modelNumber'],
                                'upc': item['upc'],
                                'image_urls': [item['largeImage']],
                                'thumbnail': item['thumbnailImage']
                            },
                            {
                                'vendor': self.vendor,
                                'price': item['salePrice'],
                                'url': item['productUrl']
                            }
                        ]
                    )
                except KeyError:
                    pass
                
            try:
                if iter >= count:
                    break
                response=requests.get('http://api.walmartlabs.com' + response.json()['nextPage'])
                #print(response.json()['nextPage'])
                self.log(response.json()['nextPage'])
                iter += 1
            except (KeyError, json.decoder.JSONDecodeError):
                break

        return product_list