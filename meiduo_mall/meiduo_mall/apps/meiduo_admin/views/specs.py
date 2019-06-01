from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SPUSpecification
from meiduo_admin.serializer.specs import GoodsSpecsSerializer
from meiduo_admin.utils.pagination import MiddlePagination


class GoodsSpecsViewSet(ModelViewSet):
    """/goods/specs/"""
    permission_classes = {IsAdminUser}
    def get_serializer_class(self):

        if self.request.data.get("goods_id"):
            self.request.data["spu_id"] = self.request.data.get("goods_id")
            del self.request.data["goods_id"]
        return GoodsSpecsSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = MiddlePagination
