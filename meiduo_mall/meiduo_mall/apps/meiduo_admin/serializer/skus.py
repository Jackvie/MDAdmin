from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView

from goods.models import SKUImage, SKU, SKUSpecification, GoodsCategory, SPU, SpecificationOption
from meiduo_mall.utils.fdfs.storage import FDFSStorage


class SKUImageSerializer(serializers.ModelSerializer):
    """SKU图片序列化器类"""
    sku = serializers.StringRelatedField(label="SKU商品名称")
    sku_id = serializers.IntegerField(label="SKU_ID")
    class Meta:
        model = SKUImage
        fields = ("image", "sku", "sku_id", "id")

    def validate_sku_id(self, value):
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError("SKU不存在")
        return sku

    def create(self, validated_data):
        """保存图片"""
        file = validated_data.get("image")
        # 上传文件到FDFS系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception as e:
            print(e)
            raise APIException('上传文件FDFS系统失败')
        sku = validated_data.get("sku_id")
        sku_image = SKUImage.objects.create(
            sku=sku,
            image=file_id
        )
        if not sku.default_image:
            sku.default_image = sku_image.image.url
            sku.save()

        return sku_image

    def update(self, instance, validated_data):
        file = validated_data.get("image")
        # 上传文件到FDFS系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
            print(file_id)
        except Exception as e:
            print(e)
            raise APIException('上传文件FDFS系统失败')

        instance.image = file_id
        instance.save()

        return instance


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""
    class Meta:
        model = SKU
        fields = ("id", "name")


class SKUSpecSerializer(serializers.ModelSerializer):
    """商品规格信息序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')
    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""

    spu = serializers.StringRelatedField(label="商品SPU名称")
    category = serializers.StringRelatedField(label="三级分类名称")
    category_id = serializers.IntegerField(label="三级分类id")
    spu_id = serializers.IntegerField(label="商品SPU ID")
    specs = SKUSpecSerializer(label='商品规格信息', many=True)
    class Meta:
        model = SKU
        exclude = ("create_time", "update_time", "default_image")

    def validate(self, attrs):
        # 获取category_id, spu_id
        category_id = attrs['category_id']
        spu_id = attrs['spu_id']
        try:
            category = GoodsCategory.objects.get(id=category_id)
            spu = SPU.objects.get(id=spu_id)
        except Exception:
            raise serializers.ValidationError("spu or category does not exist")
        # 校验spu.category3_id是否等于category_id
        if spu.category3_id != category_id:
            raise serializers.ValidationError('SPU分类信息错误')

        # 检查sku规格数据是否有效
        spu_specs = spu.specs.all()
        spec_count = spu_specs.count()
        specs = attrs['specs']
        # SKU商品的规格数据是否完整
        if spec_count > len(specs):
            raise serializers.ValidationError('SKU规格数据不完整')
        # SKU商品的规格数据是否一致
        spu_specs_ids = [spec.id for spec in spu_specs]
        specs_ids = [spec.get('spec_id') for spec in specs]
        if spu_specs_ids.sort() != specs_ids.sort():
            raise serializers.ValidationError('商品规格数据有误')

        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            # 检查spec_id对应的规格是否包含option_id对应的选项
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            options_ids = [option.id for option in options]

            if option_id not in options_ids:
                raise serializers.ValidationError('规格选项数据有误')
        return attrs

    def create(self, validated_data):
        """保存sku商品数据"""
        specs = validated_data.pop("specs")
        with transaction.atomic():
            # 调用父类方法新增sku商品
            sku = super().create(validated_data)
            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )
        return sku

    def update(self, instance, validated_data):
        """修改sku商品数据"""
        specs = validated_data.pop('specs')
        # 获取sku商品的规格信息
        sku_specs = [{
            'spec_id': spec.spec_id,
            'option_id': spec.option_id
        } for spec in instance.specs.all()]

        with transaction.atomic():
            # 调用父类方法新增sku商品
            sku = super().update(instance, validated_data)

            # 保存商品规格信息
            if specs != sku_specs:
                # 清除sku原有的规格信息
                sku.specs.all().delete()
                for spec in specs:
                    SKUSpecification.objects.create(
                        sku=sku,
                        spec_id=spec.get('spec_id'),
                        option_id=spec.get('option_id')
                    )
        return sku

class CategorySimpleSerializer(serializers.ModelSerializer):
    """分类序列化器类"""
    class Meta:
        model = GoodsCategory
        fields = ("id", "name")



