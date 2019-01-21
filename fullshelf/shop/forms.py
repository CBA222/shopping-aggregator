from django import forms
from .models import ProductCategory

class SearchBar(forms.Form):
    query = forms.CharField(
        max_length=400,
        widget=forms.TextInput(attrs={'placeholder': 'Enter product name, model number, URL, etc'})
        )

class DisplayItems(forms.Form):
    items_per_page = forms.ChoiceField(
        widget = forms.Select(attrs={'onChange':'form.submit()'}),
        choices = [(25, 25), (50, 50), (100, 100)]
    )

    sort_items = forms.ChoiceField(
        widget=forms.Select(attrs={'onChange':'form.submit()'}),
        choices=[('relevant', 'Relevant'), ('price_ascending', 'Price-Low to high'), ('price_descending', 'Price-High to low')]
    )

class Filters(forms.Form):
    price_range = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[('0-20', '$0 to $20'), ('20-50', '$20 to $50'), ('50-100', '$50 to $100'), ('100-999999', '$100 and above')]
        )

class SearchForm(forms.Form):
    query = forms.CharField(label='search_query', max_length=400)
    filter_categories = forms.ChoiceField()