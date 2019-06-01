from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializer.brands import GoodsBrandsSerializer
from meiduo_admin.utils.pagination import SmallPagination

# /goods/brands/
class GoodsBrandsViewSet(ModelViewSet):
    """Brand"""
    permission_classes = [IsAdminUser]
    serializer_class = GoodsBrandsSerializer
    queryset = Brand.objects.all()
    pagination_class = SmallPagination
