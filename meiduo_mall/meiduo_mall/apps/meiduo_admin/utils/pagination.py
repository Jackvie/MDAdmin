from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultPagination(PageNumberPagination):
    """自定义分页类"""
    page_size = 2  # 默认页容量
    page_size_query_param = "pagesize"  # url参数可以指定页容量
    max_page_size = 5  # 最大页容量
    page_query_param = "page"  # 指定第几页的关键字　默认为page

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))


class SmallPagination(StandardResultPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('list', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))


class MiddlePagination(StandardResultPagination):
    def get_paginated_response(self, data):
        """更新返回给前端的OrderDict"""
        for every_dict in data:
            every_dict["goods"]=every_dict.pop('spu')
            every_dict["goods_id"]=every_dict.pop('spu_id')

        return Response(OrderedDict([
            ('list', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))
