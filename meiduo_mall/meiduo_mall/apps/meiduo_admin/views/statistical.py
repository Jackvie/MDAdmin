from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from goods.models import GoodsVisitCount
from meiduo_admin.serializer.statistical import GoodsVisitSerializer
from users.models import User

# GET /meiduo_admin/statistical/total_count/
class UserTotalCountView(APIView):
    """用户总数统计"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """获取网站总用户数:"""
        count = User.objects.count()
        now_date = timezone.now()

        context = {
            "count": count,
            "date": now_date.date()
        }
        return Response(context)

# GET /meiduo_admin/statistical/day_increment/
class UserDayCountView(APIView):
    """日增用户统计"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_date).count()
        context = {
            "count": count,
            "date": now_date.date()
        }
        return Response(context)


# GET /meiduo_admin/statistical/day_active/
class UserActiveAcountView(APIView):
    """日活跃用户"""
    permission_classes = [IsAdminUser]
    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        context = {
            "count": count,
            "date": now_date.date()
        }
        return Response(context)


# GET /meiduo_admin/statistical/day_orders/
class UserOrderCountView(APIView):
    permission_classes = [IsAdminUser]
    """日下单用户量"""
    def get(self, request):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).count()
        context = {
            "date": now_date.date(),
            "count": count
        }
        return Response(context)


# GET /meiduo_admin/statistical/month_increment/
class UserMonthCountView(APIView):
    """30天日增用户统计"""
    permission_classes = [IsAdminUser]

    def get(self, request):

        # 1. 获取当月每日新增用户数据
        # 当前日期
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 起始日期
        begin_date = now_date - timezone.timedelta(days=29)

        # 统计数据列表
        count_list = []

        for i in range(30):
            # 当天时间和下一天时间
            cur_date = begin_date + timezone.timedelta(days=i)
            next_date = cur_date + timezone.timedelta(days=1)

            # 统计当天新增用户数量
            count = User.objects.filter(date_joined__gte=cur_date, date_joined__lt=next_date).count()
            count_list.append({
                'date': cur_date.date(),
                'count': count
            })

        # 2. 返回应答
        return Response(count_list)


# GET /meiduo_admin/statistical/goods_day_views/
class GoodsDayView(APIView):
    """日分类商品访问量"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ [
        {
            "category": "分类名称",
            "count": "访问量"
        },
        {
            "category": "分类名称",
            "count": "访问量"
        },
        ]"""
        context = list()
        now_date = timezone.now().date()
        goods_visit = GoodsVisitCount.objects.filter(date=now_date)

        serializer = GoodsVisitSerializer(goods_visit, many=True)

        return Response(serializer.data)
