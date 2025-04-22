
from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse, HttpRequest
from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import  (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, 
    GenericAPIView
    )
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from store.filters import CollectionFilter, ProductFilter

from .models import Collection, OrderItem, Product, Review
from .serializers import (
    CollectionModelSerializer,
    CollectionSerializer,
    ProductSerializer,
    ProductModelSerializer,
    ReviewSerializer
    )


# ViewSets

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ["collection_id"]
    filterset_class = ProductFilter
    
    
    # Completely remove the ff after setting up django_filters
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get("collection_id")
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    def get_serializer_context(self):
        return { "request":self.request }
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
           return Response({'Error':"Product cannot be deleted because it has an association with order"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)     
        return super().destroy(request, *args, **kwargs)
    
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products"))
    serializer_class = CollectionModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter
    
    
    def update(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=kwargs['pk'])
        collection_serializer = CollectionModelSerializer(collection,data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return super().update(request, *args, **kwargs)
    
    # def put(self, request:Request, pk:int)->Response:
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=pk)
    #     collection_serializer = CollectionModelSerializer(collection,data=request.data)
    #     collection_serializer.is_valid(raise_exception=True)
    #     collection_serializer.save()
    #     return Response(data=collection_serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({"error":"Collection cannot be deleted because it has an association with products"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request:Request,pk:int)->Response:
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=pk)
    #     if collection.products.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
        
    
    def get_serializer_context(self):
        return {"product_id":self.kwargs['product_pk']}
    
    
# Generic views

class ProductListCreateView(ListCreateAPIView):
    
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductModelSerializer
    
    # if you don't have a logic(some calculation) 
    # to define use the above other stick with the following two methods
    
    # def get_queryset(self):
    #     return Product.objects.select_related("collection").all()
    
    # def get_serializer_class(self):
    #     return ProductModelSerializer
    
    def get_serializer_context(self):
        return { "request":self.request }
    
    
class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = ProductModelSerializer
     
    def get_queryset(self):
        return Product.objects.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get("pk")
        
        try:
            return queryset.get(pk=pk)
        except Product.DoesNotExist:
            return NotFound("Product Not Found!!!")
        
    def get_serializer_context(self):
        return { 'request':self.request }
    
    
class CollectionListCreateView(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionModelSerializer
    
    # def get_queryset(self):
    #     return Collection.objects.annotate(products_count=Count("products")).all()
    
    # def get_serializer_class(self):
    #     return CollectionModelSerializer
    
    
    
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


class ProductDetailRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = "id"
    
    def delete(self, request:Request, id:int)->Response:
        product = get_object_or_404(Product,pk = id)
        if product.orderitems.count() > 0:
           return Response({'Error':"Product cannot be deleted because it has an association with order"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)     
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
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
           return Response({"error":"Product cannot be deleted because it has an association with orders"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
        

class CollectionDetailRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    
    def put(self, request:Request,pk:int)->Response:
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")), pk=pk)
        collection_serializer = CollectionModelSerializer(collection,data=request.data)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()
        return Response(collection_serializer.data)
    
    def delete(self,request:Request, pk:int)->Response:
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")),pk=pk)
        if collection.products.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
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
