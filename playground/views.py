from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q as Query,F as Reference

from store.models import Order, Product, OrderItem, Customer

#  A view: request handle in python not in other languages
# takes(input) => return(output)
# request => response
# action

def basic_filtering_and_retrieving():
    # The all() method returns all entries in the database also colled the manager object
    queryset = Product.objects.all() # get all the products from the database
    
    # A scenario where the querset is evaluated
    # When the queryset is iterated over it
    # Whent it accessed by its index i.e queryset[0], queryset[1:9]
    # When it is converted to a list i.e list(queryset)
    
    # Get all products
    # products = Product.objects.all()
    
    # Get single product
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    
    # Alternative for the above code
    product = Product.objects.filter(pk=0).first() # returns None if the object does not exist
    
    # check_if_exists = Product.objects.filter(pk=0).exists() # returns True or False
    
    product = Product.objects.filter(unit_price=100)
    products = Product.objects.filter(unit_price__gt=100) # greater than 100
    products = Product.objects.filter(unit_price__range=(10,1000)) # greater than 100
    products = Product.objects.filter(collection__id=10) # greater than 100
    products = Product.objects.filter(collection__id__range=(10,20)) # greater than 100
    
    products = Product.objects.filter(title__contains="coffee") # case sensitive
    products = Product.objects.filter(title__icontains="coffee") # case insensitive
    products = Product.objects.filter(title__startswith='apple')
    products = Product.objects.filter(title__istartswith='apple')
    products = Product.objects.filter(title__endswith='fruit')
    products = Product.objects.filter(title__iendswith='fruit')
    
    products = Product.objects.filter(last_update__date='2024-02-01')
    products = Product.objects.filter(last_update__date__gt='2024-02-01')
    products = Product.objects.filter(last_update__date__lt='2024-11-11')
    
    # products = Product.objects.filter(desctiption__isnull=True)
    
    return products


def complex_filtering():
    # AND
    products = Product.objects.filter(unit_price__gt=100, inventory__lt=200) # one option
    products = Product.objects.filter(unit_price__gt=100).filter(inventory__lt=200)# the other option
    # products = Product.objects.filter(Query(unit_price__gt=100) & Query(inventory__lt=200))
    # OR
    products = Product.objects.filter(Query(unit_price__gt=100)| Query(inventory__lt=200))
    
    # NOT
    products = Product.objects.filter(~(Query(unit_price=100)|Query(inventory__lt=200)))
    # products = Product.objects.filter(~(Query(unit_price=100)& Query(inventory__lt=200)))
    return products

def reference_feild_filtering():
    products =  Product.objects.filter(unit_price=Reference('inventory'))
    products =  Product.objects.filter(inventory=Reference('collection__id')) # Related table
    return products

def sorting():
    products = Product.objects.order_by("title") # Ascending order
    products = Product.objects.order_by("-title") # Descending order
    
    products = Product.objects.order_by("unit_price",'-title') # ASC order with unit_price and DESC order with title
    products = Product.objects.order_by("unit_price", "-title").reverse() # DESC order with unit_price and ASC order with title
    products = Product.objects.filter(collection_id__lt=10).order_by("title")
    
    product = Product.objects.order_by("unit_price")[0] # single product
    product = Product.objects.earliest("unit_price") # single product
    product = Product.objects.latest("unit_price") # single product
    return products
    
def limiting_products():
    # Getting products with index
    # 0, 1, 2,3, 4
    products = Product.objects.all()[:5]
    
    # 5, 6, 7, 8, 9
    products = Product.objects.all()[5:10]
    
    # 100,101,...
    products = Product.objects.all()[100:]
    return products

def selecting_fields_to_query():
    products = Product.objects.values("id","title")
    
    # Returns list of dicrionaries
    products = Product.objects.values("id", "title", "collection__title") # Inner join 
    
    products = Product.objects.values_list("id","title","collection__title")
    
    # products = Product.objects.values('id','title','orderitem__id').distinct().order_by("title")
    # products_id = OrderItem.objects.values("product__id") # Getting products id from the OrderItem table
    products = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).values("id","title","orderitem__id").order_by('title')
    return products

def selecting_with_only_and_defer():
    # Don't do the following if you don't know what you are doing
    # don't use the following specially if you are using loops to render multiple column
    products = Product.objects.only("id","title") # return only id, and title
    products = Product.objects.defer("description") # return all columns except description
    return products

def selecting_related_objects():
    # Don't do the following to select related objects
    # products = Product.objects.all()
    
    # Instead do the following
    # use selected_related for on instance(1)
    products = Product.objects.select_related().all()
    # products = Product.objects.select_related("collection__someOtherRelatedField").all()
    
    # use prefetch_related for many objects(n)
    products = Product.objects.prefetch_related("promotions").all()
    
    # the following 2 line of codes are exactly the same
    products = Product.objects.prefetch_related("promotions").select_related("collection").all()
    products = Product.objects.select_related("collection").prefetch_related("promotions").all()
    
    customer_id = Order.objects.values("customer_id").distinct()
    order_id = OrderItem.objects.values("order_id").distinct()
    
    orders = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]
    return orders

def say_hello(request):
    # products = basic_filtering_and_retrieving()
    # products = complex_filtering()
    # products = reference_feild_filtering()
    
    # products = sorting()
    
    # products = limiting_products()
    
    # products = selecting_fields_to_query()
    
    # products = selecting_with_only_and_defer()
    
    products = selecting_related_objects()
    
    return render(request, "hello.html",{"name":"Demis","products":list(products)})

