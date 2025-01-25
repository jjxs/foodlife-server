
from rest_framework.serializers import ModelSerializer
from master.models.role import *

################################## シリアル ########################################


class RoleDetailSerializer(ModelSerializer):
    class Meta:
        model = RoleDetail
        fields = ('__all__')


class RoleSerializer(ModelSerializer):
    details = RoleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('name', 'details')
