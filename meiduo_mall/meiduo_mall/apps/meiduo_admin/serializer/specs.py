from rest_framework import serializers

from goods.models import SPUSpecification, SPU


class SPUSimpleSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = SPU
        fields = ("id", "name")

class GoodsSpecsSerializer(serializers.ModelSerializer):
    """规格"""
    spu = serializers.StringRelatedField(label="b")
    spu_id = serializers.IntegerField(label="a")
    class Meta:
        model = SPUSpecification
        fields = ("id", "name", "spu", "spu_id")
