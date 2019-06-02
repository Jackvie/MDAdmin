from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializer.permissions import PermissionSerializer, ContentTypeSerializer, GroupSerializer
from meiduo_admin.serializer.permissions import AdminSerializer
from users.models import User


# GET /meiduo_admin/permission/perms/
class PermissionViewSet(ModelViewSet):
    """获取用户权限表列表数据"""
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.action == "content_type":
            return ContentType.objetcs.all()
        else:
            return Permission.objects.all()

    def get_serializer_class(self):
        if self.action == "content_type":
            return ContentTypeSerializer
        else:
            return PermissionSerializer

    # GET /meiduo_admin/permission/content_types/
    def content_types(self, request):
        self.pagination_class = None
        return self.list(request)


# GET /meiduo_admin/permission/groups/
class GroupViewSet(ModelViewSet):
    """获取用户组表列表数据"""
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # GET /meiduo_admin/permission/simple/
    def simple(self, request):
        queryset = Permission.objects.all()
        serializer = PermissionSerializer(queryset, many=True)
        return Response(serializer.data)


# GET /meiduo_admin/permission/admins/
class AdminViewSet(ModelViewSet):
    """"""
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer

    # GET /meiduo_admin/permission/groups/simple/
    def simple(self, request):
        """获取用户组数据"""
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

