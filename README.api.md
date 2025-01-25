
# SQL
1. SQLのファイル名で利用

    app/sql/find_seat_list.sql => SQL("find_seat_list") OR SQL("find_seat_list", appname)

    ※注意：【--確認済み分取得】のようなコメントをファイルにのこさない

2. SQL分そのまま利用

```python
    seat_list = SeatList.objects.raw('''
    SELECT
        seat.id　※idは必須項目
        , seat_no
        , seat.name
        , seat.start
        , usable
        , seat.number
        , seat_type_id as seat_type
        , seat_smoke_type_id as seat_smoke_type
        , seat_group.no as group_no
        , seat_group.name as group_name
    FROM
         seat left join seat_group on seat_group.id = seat.group_id
    ''')
```

# API 

1. SampleAPIView SeatController(APIView):
    defの定義は制限なし、URL定義は固定

```python
    # url定義「(?P<fun>.*)」部分は固定
    urlpatterns = [
        ...
        url(r'^menu/(?P<fun>.*)/', MenuController.as_view()),
    ]
```

2. APIView　　　　class SeatController(APIView):
    ※defの定義はpost get delete putのみとなり、利用不便

3. ModelViewSet  class MasterDataController(viewsets.ModelViewSet): 

```python

# 例：
class SeatListSerializer(ModelSerializer):
    '''
    SeatDataとマスタ関連データのすべて
    '''
    # 外部key項目
    # 席種別
    #seat_type = models.ForeignKey(MasterData, related_name='seat_type', null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.seat_type})

    seat_type_name = ReadOnlyField(source='seat_type.display_name', read_only=True)
    seat_smoke_type_name = ReadOnlyField(source='seat_smoke_type.display_name', read_only=True)
    group_no = ReadOnlyField(source='group.no', read_only=True)
    group_name = ReadOnlyField(source='group.name', read_only=True)

    class Meta:
        model = Seat
        fields = (
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

```

# 認証：
1. permission_classes


```python

# すべてOK（原則利用しない、事前相談）：
class SeatListController(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    ...

# 認証済みのみ：
class SeatGroupController(viewsets.ModelViewSet):

    permissions = (UserRoleAuthenticated,)
    ...

```

# よく利用する import 
1. from django.views.decorators.csrf import csrf_exempt
2. from django.http import HttpResponse, JsonResponse
3. from django_filters import rest_framework as filters
4. from rest_framework import viewsets, permissions
5. from rest_framework.response import Response
6. from rest_framework.pagination import PageNumberPagination
7. from django.core.paginator import Paginator

```python
    # 例：
    from django.db import transaction

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework.decorators import action, api_view, permission_classes
    from rest_framework import authentication, permissions, serializers

    from master.models.guest import Guest, GuestUser
    from master.models.seat import Seat, SeatStatus, SeatHistory
    from master.serializer.seat import SeatSerializer, SeatStatusSerializer

    from common.sql import SQL
    from common.util import Util
    from common.log import logger
    from common.web.json import JsonResult
    from common.views.view import BaseAPIView
    from common.permission.controller import UserRoleAuthenticated
```

