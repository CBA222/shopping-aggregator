from search_engine.search_interface import SearchInterface

search_path = 'http://127.0.01:9200'
db_path = 'postgresql://postgres:lego_10010@localhost/product_database_2'

si = SearchInterface(search_path, db_path)
si.setup()