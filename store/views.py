from django.shortcuts import render
# from django.http import HttpResponse, HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Built in
# def product_list(request:HttpRequest)->HttpResponse:
#     return HttpResponse("OK.")


# Restframework
@api_view()
def product_list(request: Request) -> Response:
    return Response("Ok.")
    

@api_view()
def product_detail(request:Request,id:int) -> Response:
    return Response(id)
    