
# GET /meiduo_admin/goods/simple/
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db.models import Q

from goods.models import SPU, SPUSpecification, Brand, GoodsCategory
from meiduo_admin.serializer.spus import SPUSimpleSerializer, SPUSpecSerializer, GoodsSerializer, \
    GoodsBrandsSimpleSerializer, GoodsChannelCategoriesSerializer, GoodsChannelCategoriesSerializer23
from meiduo_admin.utils.pagination import SmallPagination


class SPUSimpleView(ListAPIView):
    """获取spu表名称数据"""
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer

    pagination_class = None


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecView(ListAPIView):
    """获取SPU商品规格信息"""

    permission_classes = [IsAdminUser]
    def get_queryset(self):
        queryset = SPUSpecification.objects.filter(spu_id=self.kwargs["pk"])
        return queryset
    serializer_class = SPUSpecSerializer
    # 注：关闭分页
    pagination_class = None

# class SPUSpecView(GenericAPIView):
#     """获取SPU商品规格信息"""
#
#     permission_classes = [IsAdminUser]
#     def get(self, request, pk):
#         spus = SPUSpecification.objects.filter(spu_id=pk)
#         serializer = SPUSpecSerializer(spus, many=True)
#         pagination_class = None
#         return Response(serializer.data)

# /goods/
class GoodsViewSet(ModelViewSet):
    """SPU序列化器类"""
    permission_classes = [IsAdminUser]
    serializer_class = GoodsSerializer
    queryset = SPU.objects.all()

    pagination_class = SmallPagination


# goods/brands/simple/
class GoodsBrandsSimpleView(ListAPIView):
    """"""
    permission_classes = [IsAdminUser]
    serializer_class = GoodsBrandsSimpleSerializer
    queryset = Brand.objects.all()
    pagination_class = None


# goods/channel/categories/
class GoodsChannelCategoriesViewSet(ReadOnlyModelViewSet):
    """{
                "id": "分
                "name":
                "subs": [
                ]
    }"""
    permission_classes = [IsAdminUser]
    def get_serializer_class(self):
        if self.action == "list":
            return GoodsChannelCategoriesSerializer
        else:
            return GoodsChannelCategoriesSerializer23
    def get_queryset(self):
        if self.kwargs.get("pk"):
            category = GoodsCategory.objects.filter(~Q(subs=None))
        else:
            category = GoodsCategory.objects.filter(parent__isnull=True)
        return category
    pagination_class = None
