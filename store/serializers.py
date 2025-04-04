from dataclasses import field
from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    

# Instead of redefining all 
# Use the following
class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']

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
    
    # Serializing relationships
    # Primary key
    # String related file
    # Nested Object
    # Hyperlink
    
    
    
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    
    
    # Instead of redefining all 
    # the fields inside ProductSerializer we can do the following
    
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','price','price_with_tax','collection']
        
        # You mustn't do the following because
        #  if tomorrow we add field that field 
        # will expose to the outside world which 
        # may contain sensitive data,
        # Actually this is the behavior of lazy devs.
        # Generally you have to explicitely set the fields like what I did above
        # fields = '__all__'
    
    # If you want to change something do the following 
    # otherwise stick with the original one
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    
    collection = CollectionModelSerializer()
    
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    
    def calculate_tax(self, product:Product) -> Decimal:
        return product.unit_price * Decimal(1.1)
    
    # this validation do not make sense here 
    # but I wanna put here to make sure that
    # we can also validate the data
    # def validate(self, data):
    #     if data['password'] != data['comfirm_password']:
    #         return serializers.ValidationError("Passwords do not match!!")
    #     return data