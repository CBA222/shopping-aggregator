from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Product, ProductCategory, Vendor
from .forms import Filters, DisplayItems
from .helpers import search

def index(request):
    context = {
        'main_menu': ['Electronics', 'Home Goods', 'Fashion', 'Entertainment', 'Cosmetics'],
    }
    return render(request, 'shop/index.html', context)

def product_page(request, product_id):
    product = Product.objects.get(id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'shop/product_page.html', context)
    

def search_results(request, page_number):
    pages_to_show = 9

    query = request.GET['query']
    #full_product_list = Product.objects.filter(name__icontains=query)
    full_product_list = search(query, Product.objects.all())
    vendor_list = Vendor.objects.all()

    price_range = request.GET['price_range']
    if price_range != 'all':
        div_idx = price_range.find('-')
        lowest_price = int(price_range[0:div_idx])
        highest_price = int(price_range[div_idx+1:])
        full_product_list = full_product_list.filter(best_price__gte=lowest_price, best_price__lte=highest_price)

    sort_order = request.GET['sort_items']
    if sort_order == 'price_ascending':
        full_product_list = full_product_list.order_by('best_price')
    elif sort_order == 'price_descending':
        full_product_list = full_product_list.order_by('-best_price')

    items_per_pages = int(request.GET['items_per_page'])
    num_pages = int(len(full_product_list) / items_per_pages)
    
    paginator = Paginator(full_product_list, items_per_pages)
    product_list = paginator.get_page(page_number)

    if page_number < (pages_to_show / 2):
        if num_pages < pages_to_show:
            page_number_list = range(1, num_pages + 1)
        else:
            page_number_list = range(1, pages_to_show + 1)
    else:
        if num_pages < (int(page_number + (pages_to_show / 2))):
            page_number_list = range(int(page_number - (pages_to_show / 2) + 1), num_pages + 1)
        else:
            page_number_list = range(int(page_number - (pages_to_show / 2) + 1), int(page_number + (pages_to_show / 2) + 1))

    context = {
        'query': query,
        'product_list': product_list,
        'vendor_list': vendor_list,
        'page_number_list': page_number_list,
        'current_page': page_number,
        'DisplayItems': DisplayItems(initial={'items_per_page': request.GET['items_per_page'], 'sort_items': request.GET['sort_items']}),
        'Filters': Filters(initial={'price_range': request.GET['price_range']})
    }

    return render(request, 'shop/search_results.html', context)

