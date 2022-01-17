from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .py.searching_algorithm import ProductsSearching
from .models import Product
# from .filters import ProductFilter


def index(request):
    a = Product.objects.order_by('-y')

    search_query = request.GET.get("search", "").strip()
    print(search_query)
    context = {
        'queryset': a,
    }

    if search_query:
        result = ProductsSearching(search_query).return_products()
        if result is None:
            return render(request, 'main/search-no-results.html', {"searchName": search_query})

        products = result[0]
        categories = result[1]
        brands = result[2]
        return render(request, 'main/search.html', {"a": a, "searchName": search_query, "products": products, "categories": categories, "brands": brands, "file": 0})
    else:
        return render(request, 'main/index.html')

# def search(request):
#     search_query = request.GET.get("search", "")
#     if search_query:
#         return render(request, 'main/search.html', {"name": search_query})
#     else:
#         return render(request, 'main/index.html')
