
from codecs import lookup
from django.urls import include, path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from . import views

# Nested routers

router = SimpleRouter()
router.register("products",views.ProductViewSet)
router.register("collections",views.CollectionViewSet)

review_router = NestedSimpleRouter(router,"products",lookup='product')

review_router.register("reviews",views.ReviewViewSet,basename="product-reviews")

urlpatterns = [
    path("",include(router.urls)),
    path("",include(review_router.urls))
]


# router = SimpleRouter()
# router.register("products",views.ProductViewSet)
# router.register("collections",views.CollectionViewSet)

# urlpatterns = router.urls


# Default Router -> adds to extra functioinality

# router = DefaultRouter()
# router.register("products",views.ProductViewSet)
# router.register("collections",views.CollectionViewSet)

# urlpatterns = router.urls



# URLConfig
# urlpatterns = [
#     path("products/", views.ProductListCreateView.as_view()),
#     # path("products/<int:id>/",views.ProductDetail.as_view()),
#     path("products/<int:id>/",views.ProductDetailRetrieveUpdateDestroyAPIView.as_view()),
#     path("collections/",views.CollectionListCreateView.as_view()),
#     # path("collections/<int:pk>/",views.CollectionDetail.as_view(), name='collection-detail')
#     path("collections/<int:pk>/",views.CollectionDetailRetrieveUpdateDestroyAPIView.as_view(), name='collection-detail')
# ]
