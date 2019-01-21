import requests

class SearchQueryInterface:
    """
    This class provides methods of searching the search index
    """

    def __init__(self, index_path):
        self.search_request_path = '{}/{}'.format(index_path, '_search?pretty')

    def search(self, query, category_filter=None, sort_by=None, page_size=10, return_fields=['db_id']):
        response = requests.get(
            self.search_request_path,
            json={
                'from': 0, 'size': page_size,
                'query': {
                    'bool': {
                        'must': [
                            { 
                                'multi_match': {
                                    'query': query,
                                    'type': 'most_fields',
                                    'fields': return_fields
                                }
                            }
                        ],
                        'filter': [
                            { 
                                'term': { 
                                    'category': category_filter 
                                }
                            }
                        ]
                    }
                }
            }
        )

        return response

        