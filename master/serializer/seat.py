from rest_framework.serializers import ModelSerializer, ReadOnlyField, DateTimeField

from master.models.seat import SeatGroup, SeatStatus, Seat


class SeatGroupSerializer(ModelSerializer):

    class Meta:
        model = SeatGroup
        fields = ('__all__')


class SeatStatusSerializer(ModelSerializer):

    seat_group_no = ReadOnlyField(source='seat.group.no', read_only=True)
    seat_group_name = ReadOnlyField(source='seat.group.name', read_only=True)
    seat_no = ReadOnlyField(source='seat.seat_no', read_only=True)
    seat_name = ReadOnlyField(source='seat.name', read_only=True)
    start = DateTimeField(format='%Y/%m/%d %H:%M:%S.%f')
    end = DateTimeField(format='%Y/%m/%d %H:%M:%S.%f')

    class Meta:
        model = SeatStatus
        #　セキュリティーキーのみ提供する、他の情報はオーダー後、セキュリティーキーで検索する
        fields = ('seat',
                  'seat_group_no',
                  'seat_group_name',
                  'seat_no',
                  'seat_name',
                  'start',
                  'end',
                  'security_key')


class SeatSerializer(ModelSerializer):
    '''
    SeatDataとマスタ関連データのすべて
    '''
    seat_type_name = ReadOnlyField(source='seat_type.display_name', read_only=True)
    seat_smoke_type_name = ReadOnlyField(source='seat_smoke_type.display_name', read_only=True)
    group_no = ReadOnlyField(source='group.no', read_only=True)
    group_name = ReadOnlyField(source='group.name', read_only=True)

    class Meta:
        model = Seat
        fields = (
            'id',
            'seat_no',
            'name',
            'start',
            'usable',
            'number',
            'seat_type',
            'seat_smoke_type',
            'group',
            'seat_type_name',
            'seat_smoke_type_name',
            'group_no',
            'group_name'
        )
