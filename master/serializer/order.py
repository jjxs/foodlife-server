
from rest_framework.serializers import ModelSerializer, ReadOnlyField, DateTimeField
from master.models.order import *


class OrderDetailStatusSerializer(ModelSerializer):

    status_code = ReadOnlyField(source='status.code', read_only=True)
    status_name = ReadOnlyField(source='status.display_name', read_only=True)    
    start_time = DateTimeField(format='%Y/%m/%d %H:%M:%S.%f', read_only=True)
    class Meta:
        model = OrderDetailStatus
        fields = (
            'status',
            'status_code',
            'status_name',
            'start_time'
        )


class OrderDetailSerializer(ModelSerializer):

    order_detail_status = OrderDetailStatusSerializer(many=True, read_only=True)
    menu_no = ReadOnlyField(source='menu.no', read_only=True)
    menu_name = ReadOnlyField(source='menu.name', read_only=True)
    status_code = ReadOnlyField(source='status.code', read_only=True)
    status_name = ReadOnlyField(source='status.display_name', read_only=True)

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'order',
            'menu',
            'menu_no',
            'menu_name',
            'option',
            'count',
            'cancelable',
            'status',
            'status_code',
            'status_name',
            'order_detail_status'
        )


class OrderSerializer(ModelSerializer):

    order_detail = OrderDetailSerializer(many=True, read_only=True)

    order_type_name = ReadOnlyField(source='order_type.display_name', read_only=True)
    order_method_name = ReadOnlyField(source='order_method.display_name', read_only=True)
    user_name = ReadOnlyField(source='user.username', read_only=True)
    order_time = DateTimeField(format='%Y/%m/%d %H:%M:%S.%f', read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id',
            'order_type',
            'order_type_name',
            'order_method',
            'order_method_name',
            'seat',
            'guest',
            'user',
            'user_name',
            'order_time',
            'order_detail'
        )
