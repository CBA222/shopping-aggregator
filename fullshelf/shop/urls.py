from django.urls import path, re_path, include

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    #path('search_results', views.search_results, name='search_results'),
    path('product_page/<int:product_id>/', views.product_page, name='product_page'),
    #re_path(r'^search_results/(?P<page_number>\d+)/$', views.search_results, name='search_results'),
    path('search_results/<int:page_number>/',views.search_results, name='search_results'),

    path(r'^search/', include('haystack.urls')),
    
]