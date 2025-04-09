from .models import  Material, Users, Addresss, Cookbook, Communityss, Store, infodetail, order
from rest_framework import serializers


class Addresssr(serializers.ModelSerializer):
    class Meta:
        model = Addresss
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, }}


# 3.10


class OrderSr(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = '__all__'


class Infodetailsr(serializers.ModelSerializer):
    class Meta:
        model = infodetail
        fields = '__all__'


class StoreSr(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class CookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookbook
        fields = '__all__'


class CommunitySr(serializers.ModelSerializer):
    class Meta:
        model = Communityss
        fields = '__all__'


# 777777777777777777777777777777777777777777777777777777





class MaterialSr(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
