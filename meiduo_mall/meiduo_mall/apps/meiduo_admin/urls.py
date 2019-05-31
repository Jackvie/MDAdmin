from django.conf.urls import url

from meiduo_admin.serializer.skus import SKUSerializer
from meiduo_admin.views import users,statistical
from meiduo_admin.views.channels import ChannelViewSet, ChannelCategoriesView, ChannelTypesView
from meiduo_admin.views.skus import SKUImageViewSet, SKUSimpleView, SKUViewSet, SKUCategoriesView
from meiduo_admin.views.spus import SPUSimpleView, SPUSpecView

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
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"goods/channels", ChannelViewSet, base_name="channels")
router.register(r"skus/images", SKUImageViewSet, base_name="images")
router.register(r"skus", SKUViewSet, base_name="skus")

urlpatterns += router.urls