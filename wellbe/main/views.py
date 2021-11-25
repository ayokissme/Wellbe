from django.shortcuts import render
from .py.searching_algorithm import ProductsSearching


def index(request):
    search_query = request.GET.get("search", "")
    if search_query:
        products = ProductsSearching(search_query).return_products()
        if products is None:
            return render(request, 'main/search-no-results.html', {"searchName": search_query})
        return render(request, 'main/search.html', {"searchName": search_query, "products": products})
    else:
        return render(request, 'main/index.html')


# def search(request):
#     search_query = request.GET.get("search", "")
#     if search_query:
#         return render(request, 'main/search.html', {"name": search_query})
#     else:
#         return render(request, 'main/index.html')