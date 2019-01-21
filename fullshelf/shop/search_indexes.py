from haystack import indexes
from .models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    best_price = indexes.DecimalField(model_attr='best_price')

    def get_model(self):
        return Product