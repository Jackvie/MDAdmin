


from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializer.options import SpecsOptionsSerializer, GoodsSpecsSimpleSerializer
from meiduo_admin.utils.pagination import SmallPagination

# specs/options
class SpecsOptionsViewSet(ModelViewSet):
    """"""
    permission_classes = [IsAdminUser]
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecsOptionsSerializer

    # pagination_class = SmallPagination

# goods/specs/simple/
class GoodsSpecsSimpleView(ListAPIView):
    """
    """
    permission_classes = [IsAdminUser]
    # queryset = SPUSpecification.objects.all()

    def get_queryset(self):
        queryset = SPUSpecification.objects.all()

        for spu_spec in queryset:
            spu_spec.name = spu_spec.spu.name +":"+spu_spec.name
        return queryset

    serializer_class = GoodsSpecsSimpleSerializer
    pagination_class = None
