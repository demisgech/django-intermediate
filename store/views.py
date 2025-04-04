
from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse, HttpRequest
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .models import Collection, Product
from .serializers import CollectionModelSerializer, ProductSerializer, ProductModelSerializer


# Class based views
class ProductList(APIView):
    
    def get(self,request:Request)->Response:
        product_queryset = Product.objects.select_related("collection").all()
        product_serializer = ProductModelSerializer(product_queryset, many=True,context={"request":request})
        return Response(product_serializer.data)

    def post(self,request:Request)->Response:
        product_serializer = ProductModelSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data,status=status.HTTP_201_CREATED)    


class ProductDetail(APIView):
    def get(self, request:Request,id:int)->Response:
        product = get_object_or_404(Product,pk=id)
        product_serializer = ProductModelSerializer(product,context={'request':request})
        return Response(product_serializer.data,status=status.HTTP_200_OK)
        
    def put(self,request:Request,id:int)->Response:
        product = get_object_or_404(Product,pk=id)
        product_serializer = ProductModelSerializer(product,data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)
    
    def delete(self,request:Request,id:int)->Response:
        product = get_object_or_404(Product,pk=id)
        if product.orderitems.count() > 0:
            Response({"error":"Product cannot be deleted because it has an association with orders"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    
    def get(self, request:Request)->Response:
        collection_queryset = Collection.objects.annotate(products_count=Count("products")).all()
        collection_serializer = CollectionModelSerializer(collection_queryset,many=True)
        return Response(collection_serializer.data)
        
    def post(self,request:Request)->Response:
        collection_serializer = CollectionModelSerializer(data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return Response(collection_serializer.data,status=status.HTTP_201_CREATED)
        

class CollectionDetail(APIView):
    
    def get(self, request:Request,pk:int)->Response:
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
        collection_serializer = CollectionModelSerializer(collection)
        return Response(collection_serializer.data)
        
    def put(self, request:Request,pk:int)->Response:
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
        collection_serializer = CollectionModelSerializer(collection,data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return Response(collection_serializer.data)
    
    def delete(self, request:Request,pk:int)->Response:
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=pk)
        if collection.products.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
        
#  Function baseed views
@api_view(['GET',"POST"])
def product_list(request: Request) -> Response:
    if request.method == "GET":
        product_queryset = Product.objects.select_related("collection").all()
        products_serializer = ProductSerializer(product_queryset, 
                                                many=True,
                                                context={'request':request}
                                                )
        # products_serializer = ProductModelSerializer(product_queryset, many=True,context={"request":request} )
        return Response(products_serializer.data)
    elif request.method == "POST":
        product_serializer = ProductModelSerializer(data=request.data)  
        
        # if product_serializer.is_valid():  
        #     product_serializer.validated_data
        #     return Response("Ok.")
        # else:
        #     return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        # We can rewrite the above if...else block in a simpler way as follows
        
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        # here don't touch product_serializer.validate_data 
        # the save() method does that for us
        # print(product_serializer.validated_data)
        return Response(product_serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','DELETE'])
def product_detail(request:Request,id:int) -> Response:
    # try:
    #     product = Product.objects.get(pk=id)
    #     product_serializer = ProductSerializer(product)
    #     data = product_serializer.data
    #     return Response(data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    
    # instead of writing all the above try ... except 
    # statement with use shortcut
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        product_serializer = ProductModelSerializer(product,context={'request':request})
        return Response(product_serializer.data)
    elif request.method == "PUT":
        product_serializer = ProductModelSerializer(product,data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({'error':"Product cannot be deleted because it is associated with order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(["GET","POST"])
def collection_list(request:Request)->Response:
    if request.method == "GET":
        collection_queryset = Collection.objects.annotate(products_count=Count('products')).all()
        collection_serializer = CollectionModelSerializer(collection_queryset,many=True)
        return Response(collection_serializer.data)
    
    elif request.method == "POST":
        collection_serializer = CollectionModelSerializer(data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return Response(collection_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET","DELETE","PUT"])
def collection_detail(request:Request,pk:int)->Response:
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    if request.method == "GET":
        collection_serializer = CollectionModelSerializer(collection)
        return Response(collection_serializer.data)
    
    elif request.method == "PUT":
        collection_serializer = CollectionModelSerializer(collection, data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return Response(collection_serializer.data)
    
    elif request.method == "DELETE":
        if collection.products.count() > 0:
           return Response({"error":"Collection cannot be deleted because it includes one or more products"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
