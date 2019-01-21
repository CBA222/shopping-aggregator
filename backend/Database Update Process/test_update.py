from sql_database.dbsearch_interface import UpdateInterface
from sqlalchemy import create_engine

search_path = 'http://127.0.01:9200'
index_name = 'products'

engine = create_engine('postgresql://postgres:lego_10010@localhost/product_database_2')
conn = engine.connect()

db = UpdateInterface(conn, search_path, index_name)

store_id = 1
listings = [
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'},
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'},
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'},
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'},
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'},
    {'name': 'Dell PC', 'description': '...', 'image_urls': ['1.png','2.png'], 'thumbnail': '01.png', 'upc': '123', 'model_number': 'ABC', 'vendor': 'Wal-Mart', 'price': '0.99', 'url': 'walmart.com'}
]

db.add_store_listings(store_id, listings)


