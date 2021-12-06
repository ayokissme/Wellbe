from django.shortcuts import render
from .py.searching_algorithm import ProductsSearching


def index(request):
    search_query = request.GET.get("search", "")
    if search_query:
        result = ProductsSearching(search_query).return_products()
        products = result[0]
        categories = result[1]
        brands = result[2]
        if products is None:
            return render(request, 'main/search-no-results.html', {"searchName": search_query})
        return render(request, 'main/search.html', {"searchName": search_query, "products": products, "categories": categories, "brands": brands})
    else:
        return render(request, 'main/index.html')

# def search(request):
#     search_query = request.GET.get("search", "")
#     if search_query:
#         return render(request, 'main/search.html', {"name": search_query})
#     else:
#         return render(request, 'main/index.html')
