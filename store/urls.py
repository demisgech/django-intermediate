
from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views

# router = SimpleRouter()
# router.register("products",views.ProductViewSet)
# router.register("collections",views.CollectionViewSet)

# urlpatterns = router.urls

router = DefaultRouter()
router.register("products",views.ProductViewSet)
router.register("collections",views.CollectionViewSet)

urlpatterns = router.urls


# URLConfig
# urlpatterns = [
#     path("products/", views.ProductListCreateView.as_view()),
#     # path("products/<int:id>/",views.ProductDetail.as_view()),
#     path("products/<int:id>/",views.ProductDetailRetrieveUpdateDestroyAPIView.as_view()),
#     path("collections/",views.CollectionListCreateView.as_view()),
#     # path("collections/<int:pk>/",views.CollectionDetail.as_view(), name='collection-detail')
#     path("collections/<int:pk>/",views.CollectionDetailRetrieveUpdateDestroyAPIView.as_view(), name='collection-detail')
# ]
