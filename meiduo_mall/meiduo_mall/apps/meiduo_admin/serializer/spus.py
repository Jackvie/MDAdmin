from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption, Brand, GoodsCategory


class SPUSimpleSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""
    class Meta:
        model = SPU
        fields = ("id", "name")


class SpecOptionSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = SpecificationOption
        fields = ("id" ,"value")


class SPUSpecSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""
    # 关联对象的嵌套序列化
    spu = serializers.StringRelatedField(label='SPU名称')
    spu_id = serializers.IntegerField(label='SPU ID')

    # 关联对象的嵌套序列化
    options = SpecOptionSerializer(label='Opt选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id', 'options')


class GoodsSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""
    brand = serializers.StringRelatedField(label="品牌")
    category1_id = serializers.IntegerField(label="")
    category1 = serializers.StringRelatedField(label="")
    category2 = serializers.StringRelatedField(label="")
    category3 = serializers.StringRelatedField(label="")
    category2_id = serializers.IntegerField(label="")
    category3_id = serializers.IntegerField(label="")
    brand_id = serializers.IntegerField(label="")
    class Meta:
        model = SPU
        fields = ("id","name","brand","brand_id","category1_id","category2_id","category3_id","sales","comments","desc_detail","category1", "category2", "category3","desc_pack","desc_service")
        read_only_fields = ("sales", "comments")


class GoodsBrandsSimpleSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Brand
        fields = ("id", "name")


class GoodsChannelCategoriesSerializer(serializers.ModelSerializer):
    """Category序列化器类"""
    class Meta:
        model = GoodsCategory
        fields = ("id", "name")

class GoodsChannelCategoriesSerializer23(serializers.ModelSerializer):
    """1级序列化器23级类"""
    subs = GoodsChannelCategoriesSerializer(label="", many=True)
    class Meta:
        model = GoodsCategory
        fields = ("id", "name", "subs")