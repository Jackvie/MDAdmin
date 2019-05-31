from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet


# GET /meiduo_admin/skus/images/?page=<页码>&page_size=<页容量>
from goods.models import SKUImage, SKU, GoodsCategory
from meiduo_admin.serializer.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer, \
    CategorySimpleSerializer


class SKUImageViewSet(ModelViewSet):
    """
    {
        "counts": "图片总数量",
        "lists": [
            {
                "id": "图片ID",
                "sku": "sku商品名称",
                "sku_id": "sku商品ID",
                "image": "sku图片地址"
            },
            ...
        ],
        "page": "页码",
        "pages": "总页数",
        "pagesize": "页容量"
    }
    """
    permission_classes = [IsAdminUser]

    lookup_value_regex = "\d+"

    serializer_class = SKUImageSerializer
    queryset = SKUImage.objects.all()
    # 新增图片数据
    # {
    #     "sku_id": "sku商品ID",
    #     "image": "图片数据"
    # }


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    """获取SKU商品数据 [
        {
            "id": "sku商品ID",
            "name": "sku商品名称",
        },
        ...
    ]"""
    permission_classes = [IsAdminUser]
    serializer_class = SKUSimpleSerializer
    queryset = SKU.objects.all()

    pagination_class = None


#  GET /meiduo_admin/skus/?keyword=<名称|副标题>&page=<页码>&page_size=<页容量>
class SKUViewSet(ModelViewSet):
    """SKU视图集"""
    permission_classes = [IsAdminUser]

    # 指定router动态生成路由时，提取参数的正则表达式
    lookup_value_regex = '\d+'

    def get_queryset(self):
        """获取当前视图所使用的查询集"""
        keyword = self.request.query_params.get('keyword')

        if keyword:
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        else:
            skus = SKU.objects.all()

        return skus

    # 指定序列化器类
    serializer_class = SKUSerializer


# GET /meiduo_admin/skus/categories/
class SKUCategoriesView(ListAPIView):
    """获取第三级分类信息"""
    serializer_class = CategorySimpleSerializer

    def get_queryset(self):
        categories = GoodsCategory.objects.filter(subs=None)
        return categories

    # 注：关闭分页
    pagination_class = None


