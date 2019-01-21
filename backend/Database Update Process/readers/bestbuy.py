import requests
import json
import time
import os
import sys

from .storereader import StoreReader

def convert_to_list(data):
    s = ''
    for d in data:
        s += ','
        s += d
    return s[1:]

def load_category_ids():
    path = os.path.join(sys.path[0], 'readers/bestbuy_categories.json')
    data = []
    with open(path) as file:
        data = json.load(file)
    return [r['id'] for r in data]

class BestBuyReader(StoreReader):

    def __init__(self, apikey, page_limit = None, categories_to_skip = []):
        self.apikey = apikey
        self.vendor = 'Best Buy'
        self.page_limit = page_limit
        self.categories = load_category_ids()
        self.categories_to_skip = categories_to_skip
        
        self.attributes_to_return = ['name','modelNumber','upc','url','categoryPath.id','manufacturer','details.name','details.value','longDescription', \
        'features.feature','thumbnailImage','image','salePrice','shipping','onlineAvailability','customerReviewAverage','customerReviewCount']
        self.short_attributes_to_return = ['name', 'modelNumber', 'upc', 'salePrice', 'url', 'longDescription', 'thumbnailImage','image']
        self.pass_attributes_short = convert_to_list(self.short_attributes_to_return)

        self.base_params = 'show={}&pageSize={}&format={}&apiKey={}'.format(self.pass_attributes_short, 100, 'json', self.apikey)

        self.total_pages = 0
        self.total_products = 0

    def read_all(self):
        count = 1
        total = len(self.categories)
        product_list = []

        for c_id in self.categories:
            if c_id not in self.categories_to_skip:
                data = self.read_category(c_id, self.page_limit)
                product_list += data
                self.log("Read in {} products from category: {} ({} of {})".format(len(data), c_id, count, total))
            else:
                self.log("Skipping category: {} ({} of {})".format(c_id, count, total))
            count += 1

        return product_list

    def read_test(self):
        test_categories = ['abcat0204000']
        product_list = []

        for c in test_categories:
            product_list += self.read_category(c, self.page_limit)
        return product_list

    def read_category(self, category_id, pages_to_read = None):
        base_url = 'https://api.bestbuy.com/v1/products((categoryPath.id={}))?{}'.format(category_id, self.base_params)

        initial_response = requests.get(base_url, params={'cursorMark': '*'})
        response_json = initial_response.json()
        product_list = []
        pages_read = 0

        while True:
            try:
                if response_json['products'] == []:
                    return product_list

                for p in response_json['products']:
                    try:
                        product_list.append(
                            [
                                {
                                    'name': p['name'],
                                    'model_number': p['modelNumber'],
                                    'upc': p['upc'],
                                    'description': p['longDescription'],
                                    'thumbnail': p['thumbnailImage'],
                                    'image_urls': [p['image']]
                                },
                                {
                                    'vendor': self.vendor,
                                    'price': p['salePrice'],
                                    'url': p['url']
                                }
                            ]
                        )
                    except KeyError: 
                        pass

                pages_read += 1
                self.log('Read in {} pages from category: {}'.format(pages_read, category_id))

                if pages_to_read != None:
                    if pages_read == pages_to_read:
                        break

                next_page = response_json['nextCursorMark']
                response = requests.get(base_url, params={'cursorMark': next_page})
                response_json = response.json()

            except KeyError: 
                break
            
        return product_list