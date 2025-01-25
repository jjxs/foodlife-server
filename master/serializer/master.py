from rest_framework.serializers import ModelSerializer
from master.models.master import MasterDataGroup, MasterData


class MasterDataGroupSerializer(ModelSerializer):
    '''
    マスタグループデータのみ
    '''

    class Meta:
        model = MasterDataGroup
        fields = ('__all__')


class MasterDataSerializer(ModelSerializer):
    '''
    マスタデータのみ
    '''

    class Meta:
        model = MasterData
        fields = ('__all__')


class MasterSerializer(ModelSerializer):
    '''
    マスタデータとマスタグループデータ連携
    '''

    master_data = MasterDataSerializer(many=True, read_only=True)

    class Meta:
        model = MasterDataGroup
        fields = ('id', 'name', 'display_name', 'domain', 'master_data', 'display_order', 'extend', 'option', 'enabled')
