

from rest_framework import viewsets, permissions
from rest_framework import generics, mixins, views
from django_filters import rest_framework as filters
from master.models.menu import Menu, MenuCategory
from master.serializer.menu import *
from common.permission.controller import UserRoleAuthenticated
from common.views.view import MultipleModelViewSet
from common.filter import CharInFilter


class MenuFilter(filters.FilterSet):
    class Meta:
        model = Menu
        fields = ('__all__')


class MenuController(viewsets.ModelViewSet):

    permission_classes = (UserRoleAuthenticated,)

    serializer_class = MenuSerializer

    queryset = Menu.objects.all()

    filter_class = MenuFilter


class MenuCategoryFilter(filters.FilterSet):

    category_group = filters.CharFilter(field_name="category__group__id", lookup_expr='exact')

    class Meta:
        model = MenuCategory
        fields = ['id', 'category', 'menu', 'category_group']


class MenuCategoryController(MultipleModelViewSet):

    permission_classes = (UserRoleAuthenticated,)

    queryset = MenuCategory.objects.all().order_by('category', 'display_order')

    serializer_class = MenuCategorySerializer

    filter_class = MenuCategoryFilter


class MenuFreeFilter(filters.FilterSet):

    class Meta:
        model = MenuFree
        fields = ['id', 'menu', 'name']


class MenuFreeController(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    queryset = MenuFree.objects.all().order_by('display_order')

    serializer_class = MenuFreeSerializer

    filter_class = MenuFreeFilter


# class MenuFreeDetailFilter(filters.FilterSet):

#     menu_free__in = CharInFilter(field_name="menu_free", lookup_expr="in")

#     class Meta:
#         model = MenuFreeDetail
#         fields = ['id', 'menu_free__in']


# class MenuFreeDetailController(viewsets.ModelViewSet):

#     permission_classes = (UserRoleAuthenticated,)

#     queryset = MenuFreeDetail.objects.all()

#     serializer_class = MenuFreeDetailSerializer

#     filter_class = MenuFreeDetailFilter
