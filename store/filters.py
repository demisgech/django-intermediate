
from django_filters.rest_framework import FilterSet

from store.models import Collection, Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "collection_id":['exact'],
            "unit_price":['gt','lte']
        }

class CollectionFilter(FilterSet):
    class Meta:
        model = Collection
        fields = {
            "title":['iexact']
        }