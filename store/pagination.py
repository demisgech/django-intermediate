from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10
    

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param='page_limit'
    offset_query_param = "page_offset"
    