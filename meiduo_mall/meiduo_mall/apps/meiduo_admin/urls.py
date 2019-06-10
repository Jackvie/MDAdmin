from django.conf.urls import url

from meiduo_admin.serializer.skus import SKUSerializer
from meiduo_admin.views import users,statistical
from meiduo_admin.views.brands import GoodsBrandsViewSet
from meiduo_admin.views.channels import ChannelViewSet, ChannelCategoriesView, ChannelTypesView
from meiduo_admin.views.options import SpecsOptionsViewSet, GoodsSpecsSimpleView
from meiduo_admin.views.orders import OrdersViewSet
from meiduo_admin.views.permissions import PermissionViewSet, GroupViewSet, AdminViewSet
from meiduo_admin.views.skus import SKUImageViewSet, SKUSimpleView, SKUViewSet, SKUCategoriesView
from meiduo_admin.views.specs import GoodsSpecsViewSet
from meiduo_admin.views.spus import SPUSimpleView, SPUSpecView, GoodsViewSet, GoodsBrandsSimpleView, \
    GoodsChannelCategoriesViewSet

urlpatterns = [
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveAcountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),

    # 用户管理
    url(r'^users/$', users.UserInfoView.as_view()),
    # 频道管理
    url(r'^goods/categories/$', ChannelCategoriesView.as_view()),
    # 频道管理
    url(r'^goods/channel_types/$', ChannelTypesView.as_view()),
    # 获取SKU商品数据
    url(r'skus/simple/$', SKUSimpleView.as_view()),
    # 获取第三级分类信息
    url(r'skus/categories/$', SKUCategoriesView.as_view()),
    # 获取spu表名称数据
    url(r'^goods/simple/$', SPUSimpleView.as_view()),
    # . 获取SPU商品规格信息
    url(r'^goods/(?P<pk>\d+)/specs/$', SPUSpecView.as_view()),
    # ..for
    url(r'^goods/specs/simple/$', GoodsSpecsSimpleView.as_view()),
    #
    url(r'^goods/brands/simple/$', GoodsBrandsSimpleView.as_view()),
    #
    url(r'^permission/content_types/$', PermissionViewSet.as_view({"get":"content_types"})),
    #
    url(r'^permission/simple/$', GroupViewSet.as_view({"get":"simple"})),
    #
    url(r'^permission/groups/simple/$', AdminViewSet.as_view({"get":"simple"})),
]

from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
# router = SimpleRouter()
router.register(r"goods/channels", ChannelViewSet, base_name="channels")
router.register(r"skus/images", SKUImageViewSet, base_name="images")
router.register(r"skus", SKUViewSet, base_name="skus")
router.register(r'orders', OrdersViewSet, base_name='orders')
router.register(r'goods/brands', GoodsBrandsViewSet, base_name="brands")
router.register(r'goods/specs', GoodsSpecsViewSet, base_name="specs")
router.register(r'goods', GoodsViewSet, base_name="goods")
router.register(r'specs/options', SpecsOptionsViewSet, base_name="options")
router.register(r'goods/channel/categories', GoodsChannelCategoriesViewSet ,base_name="categories")
router.register(r'permission/perms', PermissionViewSet, base_name='permission')
router.register(r'permission/groups', GroupViewSet, base_name='group')
router.register(r'permission/admins', AdminViewSet, base_name="admin")

urlpatterns += router.urls
print(urlpatterns)
