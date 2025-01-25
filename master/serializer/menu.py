from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from master.models.menu import *


class MenuSerializer(ModelSerializer):

    stock_status_name = ReadOnlyField(source='stock_status.display_name', read_only=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'no',
            'name',
            'stock_status',
            'stock_status_name',
            'usable',
            'price',
            'note'
        )


class MenuCategorySerializer(ModelSerializer):
    '''
    マスタ関連データのすべて
    '''
    category_group = ReadOnlyField(source='category.group.id', read_only=True)
    category_name = ReadOnlyField(source='category.display_name', read_only=True)
    menu_id = ReadOnlyField(source='menu.id', read_only=True)
    menu_no = ReadOnlyField(source='menu.no', read_only=True)
    menu_name = ReadOnlyField(source='menu.name', read_only=True)
    menu_usable = ReadOnlyField(source='menu.usable', read_only=True)
    menu_price = ReadOnlyField(source='menu.price', read_only=True)

    class Meta:
        model = MenuCategory
        fields = (
            'id',
            'category',
            'menu',
            'display_order',
            'category_group',
            'category_name',
            'menu_id',
            'menu_no',
            'menu_name',
            'menu_usable',
            'menu_price',
        )


class MenuFreeDetailSerializer(ModelSerializer):

    class Meta:
        model = MenuFreeDetail
        fields = ('id', 'menu',)


class MenuFreeSerializer(ModelSerializer):

    menus = MenuFreeDetailSerializer(many=True, read_only=True)
    menu_name = ReadOnlyField(source='menu.name', read_only=True)

    class Meta:
        model = MenuFree
        fields = ('id', 'menu', 'menu_name', 'name', 'free_type', 'usable_time', 'display_order', 'menus')
