from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        source='unit_price'
        )
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # Serializeing relationships
    # option 1
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    #  option 2: but here you have select the related field 
    # otherwise you'll end up sending unnecessary queries
    # collection = serializers.StringRelatedField()
    
    # option 3
    # Using nested object
    # collection  = CollectionSerializer()
    
    # option 4
    # Create hyperlink
    
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )
    
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)