from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


class SpecsOptionsSerializer(serializers.ModelSerializer):
    """"""
    spec = serializers.StringRelatedField(label="")
    spec_id = serializers.IntegerField(label="")
    class Meta:
        model = SpecificationOption
        fields = ("id", "value", "spec", "spec_id")


class GoodsSpecsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = ("id", "name")
