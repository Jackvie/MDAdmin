from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


# GET /meiduo_admin/orders/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
from meiduo_admin.serializer.orders import OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer
from orders.models import OrderInfo


class OrdersViewSet(ReadOnlyModelViewSet):
    """分别获取订单列表和订单详情数据"""
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        else:
            return OrderDetailSerializer

    def get_queryset(self):
        # 获取搜索关键字
        keyword = self.request.query_params.get('keyword')

        if not keyword:
            return OrderInfo.objects.all()
        else:
            return OrderInfo.objects.filter(skus__sku__name__contains=keyword)

    # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        """
        修改订单状态:
        1. 校验订单是否有效
        2. 获取订单状态status并校验(status必传，status是否合法)
        3. 修改并保存订单的状态
        4. 返回应答
        """
        # 1. 校验订单是否有效
        order = self.get_object()

        # 2. 获取订单状态status并校验(status必传，status是否合法)
        serializer = OrderStatusSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)

        # 3. 修改并保存订单的状态
        serializer.save()

        # 4. 返回应答
        return Response(serializer.data