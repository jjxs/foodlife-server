from rest_framework import serializers
from restaurant.models.seat import SeatList, SeatCondition


class SeatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatList
        fields = ('__all__')


class SeatConditionSerializer(serializers.Serializer):

    seat_group = serializers.ListField(child=serializers.IntegerField())
    seat_type = serializers.ListField(child=serializers.IntegerField())
    seat_smoke_type = serializers.ListField(child=serializers.IntegerField())
    seat_number = serializers.ListField(child=serializers.CharField(allow_blank=True, allow_null=True, max_length=10))
    seat_usable = serializers.CharField(allow_blank=True, allow_null=True, max_length=10)
    takeout_type = serializers.IntegerField()

    def create(self):
        condition = SeatCondition()
        for field, value in self.validated_data.items():
            setattr(condition, field, value)
        return condition

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
