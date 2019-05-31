# GET /meiduo_admin/goods/channels/?page=<页码>&page_size=<页容量>
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

# GET /meiduo_admin/goods/channels/?page=<页码>&page_size=<页容量>
from goods.models import GoodsChannel, GoodsCategory, GoodsChannelGroup
from meiduo_admin.serializer.serializers import ChannelSerializer, CategorySimpleSerializer, ChannelGroupSerializer


class ChannelViewSet(ModelViewSet):
    """频道管理视图集"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsChannel.objects.all()

    # 指定序列化器类
    serializer_class = ChannelSerializer

# GET  `/meiduo_admin/goods/categories/`
class ChannelCategoriesView(ListAPIView):
    """频道对应一级分类视图"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsCategory.objects.filter(parent__isnull=True)
    serializer_class = CategorySimpleSerializer

    pagination_class = None

# GET /meiduo_admin/goods/channel_types/
class ChannelTypesView(ListAPIView):
    """频道组视图"""
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    queryset = GoodsChannelGroup.objects.all()

    # 指定序列化器类
    serializer_class = ChannelGroupSerializer

    # 注：关闭分页
    pagination_class = None