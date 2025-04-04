from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer, ProductModelSerializer


@api_view(['GET',"POST"])
def product_list(request: Request) -> Response:
    if request.method == "GET":
        product_queryset = Product.objects.select_related("collection").all()
        # products_serializer = ProductSerializer(product_queryset, 
        #                                         many=True,
        #                                         context={'request':request}
        #                                         )
        products_serializer = ProductModelSerializer(product_queryset, many=True,context={"request":request} )
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
        print(product_serializer.validated_data)
        return Response("ok")

@api_view()
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
    product_serializer = ProductSerializer(product)
    return Response(product_serializer.data)


@api_view()
def collection_detail(request:Request,pk:int):
    return Response(pk)    