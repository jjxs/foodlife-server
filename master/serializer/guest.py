
from rest_framework.serializers import ModelSerializer
from master.models.guest import GuestDevice, GuestUser, Guest

################################## シリアル ########################################


class GuestDeviceSerializer(ModelSerializer):
    class Meta:

        model = GuestDevice
        fields = ('__all__')


class GuestUserSerializer(ModelSerializer):
    class Meta:
        model = GuestUser
        fields = ('__all__')

# 例：　Modelそのまま利用する


class GuestDataSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ('__all__')

# 例：　Modelと関連データ連携


class GuestSerializer(ModelSerializer):
    devices = GuestDeviceSerializer(many=True, read_only=True)
    users = GuestUserSerializer(many=True, read_only=True)

    class Meta:
        model = Guest
        fields = ('sur_name', 'devices', 'users')
