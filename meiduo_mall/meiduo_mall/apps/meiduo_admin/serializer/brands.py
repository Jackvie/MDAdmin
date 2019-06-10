from rest_framework import serializers
from rest_framework.exceptions import APIException

from goods.models import Brand
from meiduo_mall.utils.fdfs.storage import FDFSStorage


class GoodsBrandsSerializer(serializers.ModelSerializer):
    """品牌序列化器类"""
    class Meta:
        model = Brand
        fields = ("id", "name", "logo", "first_letter")

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):
        logo = validated_data["logo"]
        name = validated_data["name"]
        first_letter = validated_data["first_letter"]
        try:
            fdfs = FDFSStorage()
            file_id = fdfs.save(logo.name, logo)
        except Exception as e:
            print(e)
            raise APIException("上传FDFSLOGO失败")
        brand = Brand.objects.create(
            name = name,
            logo = file_id,
            first_letter = first_letter
        )
        return brand

    def update(self, instance, validated_data):
        logo = validated_data["logo"]
        name = validated_data["name"]
        first_letter = validated_data["first_letter"]
        try:
            fdfs = FDFSStorage()
            file_id = fdfs.save(logo.name, logo)
        except Exception:
            raise APIException("上传FDFSLOGO失败")
        instance.logo = file_id
        instance.name = name
        instance.first_letter = first_letter
        instance.save()

        return instance

