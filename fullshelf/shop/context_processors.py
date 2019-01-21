from .models import ProductCategory
from .forms import SearchBar

header_categories = {
    'Apparel': ["Men's Clothing", "Women's Clothing", "Kid's Clothing", "Baby Clothing", "Shoes"],
    'Electronics': ["Computers", "Television", "Audio", "Video Games", "Software", "Accessories"]
}

categories = ['Fashion','Electronics','Books','Furniture']

def load_categories(request):

    entered_query = request.GET.get('query', '')

    return {
        #'categories': ProductCategory.objects.all(),
        'SearchBar': SearchBar(initial={'query': entered_query}),
        'header_categories': header_categories,
        'categories': categories
    }