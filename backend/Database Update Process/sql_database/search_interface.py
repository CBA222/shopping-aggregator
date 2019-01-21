import requests
from sqlalchemy import create_engine, select, or_, text

from multiprocessing import Pool
import ndjson

# encodes json for bulk update
def custom_encoder(data):
    j_str = ndjson.dumps(data)
    j_str += '\n'
    return j_str

# separates list into smaller lists of equal size
def breakup_list(data, size):
    return [data[i:i + size] for i in range(0, len(data), size)]

class SearchInterface:

    def __init__(self, search_path, index_name, process_count = 5, chunk_size = 5000):
        self.search_path = search_path
        self.index_name = index_name
        self.process_count = process_count
        self.chunk_size = chunk_size

        self.index_path_bulk = '{}/{}/{}'.format(self.search_path, self.index_name, '_bulk')

    def create_index(self):
        r = requests.put('{}/{}'.format(self.search_path, self.index_name))

        if r.status_code != 200:
            return

    def update_index(self, data):
        """
        This function updates the index with the provided data

        The data must be in a specific format:
        A list of dictionaries in the following format:
        {
            'type': 'create / update /delete',
            'data': {
                'field_1': 'value'
            }
        }
        """

        data_chunks = breakup_list(data, self.chunk_size)
        to_create = []
        to_delete = []

        for chunk in data_chunks:
            temp = []
            temp2 = []
            for row in chunk:
                if row['type'] == 'create':
                    temp.append({ "index" : { "_index" : self.index_name, "_type": "_doc" } })
                    temp.append(row['data'])
                elif row['type'] == 'delete':
                    temp2.append({ "delete" : { "_index" : self.index_name, "_type": "_doc" } })
                    temp2.append(row['data'])
            to_create.append(temp)
            to_delete.append(temp2)

        pool = Pool(self.process_count)
        pool.map(self.insert_index_bulk, to_create)
        pool.close()
        pool.join()

    def insert_index_bulk(self, chunk):
        requests.post(
            self.index_path_bulk,
            data=custom_encoder(chunk),
            headers={'Content-Type':'application/x-ndjson'}
        )