
from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListCreateView.as_view()),
    # path("products/<int:id>/",views.ProductDetail.as_view()),
    path("products/<int:id>/",views.ProductDetailRetrieveUpdateDestroyAPIView.as_view()),
    path("collections/",views.CollectionListCreateView.as_view()),
    # path("collections/<int:pk>/",views.CollectionDetail.as_view(), name='collection-detail')
    path("collections/<int:pk>/",views.CollectionDetailRetrieveUpdateDestroyAPIView.as_view(), name='collection-detail')
]
