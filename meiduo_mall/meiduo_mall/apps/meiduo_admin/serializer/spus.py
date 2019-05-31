from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption


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
    """"""
    spu = serializers.StringRelatedField(label='SPU名称')
    spu_id = serializers.IntegerField(label='SPU ID')    # 关联对象的嵌套序列化
    options = SpecOptionSerializer(label='Opt选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ("id", "name", "spu", "spu_id", "options")