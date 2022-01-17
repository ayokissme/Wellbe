from django_filters import rest_framework as filters
from wellbe.main.models import Product, Category


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    brand = CharFilterInFilter(field_name='brand')
    category = CharFilterInFilter(lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['brand', 'price', 'category']