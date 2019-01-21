from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

common_words = ['the', 'a']

def search(query, products):
    vector = SearchVector('name')
    query0 = SearchQuery(query)
    return products.annotate(rank=SearchRank(vector, query0)).order_by('-rank')
    """
    keywords = query.split()

    original_term = products.filter(name__icontains=query)
    for word in keywords:
        print(word)
        original_term = original_term.union(products.filter(name__icontains=word))

    return original_term
    """