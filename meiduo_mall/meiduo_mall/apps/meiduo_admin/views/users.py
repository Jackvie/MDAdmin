from django.db import DatabaseError
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone


# POST /meiduo_admin/authorizations/
from meiduo_admin.serializer.users import UserSerializer, AdminAuthSerializer
from users.models import User


class AdminAuthorizeView(CreateAPIView):
    # 指定当前视图所使用的序列化器类
    serializer_class = AdminAuthSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# from meiduo_admin.serializer.users import AdminAuthSerializer

# POST /meiduo_admin/authorizations/
# class AdminAuthorizeView(APIView):
#     def post(self, request):
#         """
#         管理员登录:
#         1. 获取参数并进行校验
#         2. 服务器签发jwt token数据
#         3. 返回应答
#         """
#         # 1. 获取参数并进行校验
#         serializer = AdminAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # 2. 服务器签发jwt token数据(create)
#         serializer.save()
#         print(serializer.data)
#
#         # 3. 返回应答
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
class UserInfoView(ListCreateAPIView):
    """查询用户"""
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get("keyword")
        if not keyword:
            users = User.objects.filter(is_staff=False)
        else:
            users = User.objects.filter(is_staff=False, username__contains=keyword)
        return users








