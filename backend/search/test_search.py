from search_engine.search_interface import SearchInterface

search_path = 'http://127.0.01:9200'
db_path = ''

si = SearchInterface(search_path, db_path)
r = si.search('headphone')

for row in r.json()['hits']['hits']:
    print(row['_source']['name'])