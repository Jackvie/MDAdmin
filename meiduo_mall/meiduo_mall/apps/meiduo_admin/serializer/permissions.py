from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.models import User


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器类"""
    class Meta:
        model = Permission
        fields = ("id", "name", "content_type", "codename")


class ContentTypeSerializer(serializers.ModelSerializer):
    """权限类型序列化器类"""
    class Meta:
        model = ContentType
        fields = ("id", "name")


class GroupSerializer(serializers.ModelSerializer):
    """用户组序列化器类"""
    class Meta:
        model = Group
        fields = ("id", "name", "permissions")


class AdminSerializer(serializers.ModelSerializer):
    """管理员用户序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile', 'user_permissions', 'groups', 'password')
        extra_kwargs = {
            "password":{
                'write_only': True,
               'required': False,
               'allow_blank': True
            }
        }

    def create(self, validated_data):
        """"""
        validated_data["is_staff"] = True
        user = super().create(validated_data)
        # 密码加密保存
        password = validated_data['password']
        if not password:
            # 管理员默认密码
            password = '123456abc'
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """修改管理员用户"""
        # 从`validated_data`中去除密码`password`
        password = validated_data.pop('password', None)

        # 修改管理员账户信息
        super().update(instance, validated_data)

        # 修改密码
        if password:
            instance.set_password(password)
            instance.save()

        return instance
