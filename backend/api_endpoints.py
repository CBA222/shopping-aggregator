import requests
from sqlalchemy import create_engine

class APIService:

    def __init__(self, search_url, db_path):
        self.search_url = '{}/{}'.format(search_url, '_search?pretty')
        self.db_path = db_path

    def search(self, query, filters, sort_by = None, limit = 10):
        response = requests.get(
            self.search_url,
            json={
                'query': {
                    'multi_match': {
                        'query': query,
                        'type': 'most_fields',
                        'fields': ['database_id']
                    }
                },
                'size': limit,
            }
        )

        return response

    def get_product_information(self, db_id):
        engine = create_engine(self.db_path)
        conn = engine.connect()

        info = conn.execute()
        return info
