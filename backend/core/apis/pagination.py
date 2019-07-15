"""
 * @Description:   页面数配置
 * @version         V1.0
 * @Date           2018年04月11日
"""
from rest_framework.pagination import PageNumberPagination

__all__=[
    'ChildPagination'
]


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ChildPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000
