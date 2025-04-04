from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
from store import serializers


@api_view()
def product_list(request: Request) -> Response:
    product_queryset = Product.objects.all()
    products_serializer = ProductSerializer(product_queryset, many=True)
    return Response(products_serializer.data)
    

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