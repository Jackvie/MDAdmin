
# GET /meiduo_admin/goods/simple/
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from goods.models import SPU, SPUSpecification
from meiduo_admin.serializer.spus import SPUSimpleSerializer, SPUSpecSerializer


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


