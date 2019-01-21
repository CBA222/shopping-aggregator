import requests
from sqlalchemy import create_engine, select, or_, text

from multiprocessing import Pool
import ndjson

from enum import Enum
class SORT_OPTIONS(Enum):
    PRICE = 'price'
    RELEVANCE = 'relevance'

# encodes json for bulk update
def custom_encoder(data):
    j_str = ndjson.dumps(data)
    j_str += '\n'
    return j_str

# separates list into smaller lists of equal size
def breakup_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]

class SearchInterface:

    def __init__(self, search_path, db_path, process_count = 5, chunk_size = 5000):
        self.db_path = db_path
        self.search_path = search_path
        self.index_name = 'products'
        self.process_count = process_count
        self.chunk_size = chunk_size

    def setup(self):
        r = requests.put('{}/{}'.format(self.search_path, self.index_name))

        if r.status_code != 200:
            return

        self.populate_index()

    def populate_index(self):
        """
        """
        engine = create_engine(self.db_path)
        conn = engine.connect()

        data = conn.execute(text(
            'select * from products'
        )).fetchall()

        self.index_path_bulk = '{}/{}/{}'.format(self.search_path, self.index_name, '_bulk')

        data_chunks = breakup_list(data, self.chunk_size)
        to_send = []

        for chunk in data_chunks:
            temp = []
            for row in chunk:
                temp.append({ "index" : { "_index" : self.index_name, "_type": "_doc" } })
                temp.append(
                    {
                        'db_id': row['id'],
                        'name': row['name'],
                        'description': row['description'],
                        'upc': row['upc'],
                        'model_number': row['model_number']
                    }
                )
            to_send.append(temp)

        pool = Pool(self.process_count)
        pool.map(self.insert_index_bulk, to_send)
        pool.close()
        pool.join()

    def insert_index_bulk(self, chunk):
        requests.post(
            self.index_path_bulk,
            data=custom_encoder(chunk),
            headers={'Content-Type':'application/x-ndjson'}
        )

    def search(self, query, sort_by = None, limit = 10):
        response = requests.get(
            '{}/{}/{}'.format(self.search_path, self.index_name, '_search?pretty'),
            json={
                'query': {
                    'multi_match': {
                        'query': query,
                        'type': 'most_fields',
                        'fields': ['name', 'description']
                    }
                },
                'size': limit,
            }
        )

        return response