from django.conf.urls import url

from rest_framework import routers
from app_store.api.s01.s01p01 import S01p01Api
from app_store.api.s02.s02p01 import S02p01Api
from app_store.api.s02.s02p02 import S02p02Api
from app_store.api.s03.s03p01 import S03p01Api
from app_store.api.s03.s03p02 import S03p02Api
from app_store.api.s04.s04p01 import S04p01Api
from app_store.api.store_reg.store_reg_api import StoreRegApi
from app_store.api.menu_mgmt.menu_mgmt_api import MenuMgmtApi
from app_store.api.takeout_manager.takeout_order_api import TakeoutOrderApi
from app_store.api.takeout.takeout_api import TakeoutApi
from app_store.api.ingredients.ingredients_api import IngredientsApi
from app_store.api.user_manager.user_manager_api import UserManagerApi
from app_store.api.user.user_api import UserApi
from app_store.api.seat_manager.seat_manager_api import SeatManagerApi
from app_store.api.takeout_user_manager.takeout_user_manager_api import TakeoutUserManagerApi
from app_store.api.setsubi.setsubi_api import SetsubiApi
from app_store.api.user_group.user_group_api import UserGroupApi
from app_store.api.shop_cost.shop_cost_api import ShopCostApi
from app_store.api.payment.payment_api import PaymentApi
from app_store.api.takeout.pay import PayApi
from app_store.api.menu_upload.menu_upload_api import MenuUploadApi
from app_store.api.counter.counter_api import CounterApi

router = routers.DefaultRouter()


urlpatterns = [

    url(r'^s01p01/(?P<fun>.*)/', S01p01Api.as_view()),

    url(r'^s02p01/(?P<fun>.*)/', S02p01Api.as_view()),

    url(r'^s02p02/(?P<fun>.*)/', S02p02Api.as_view()),

    url(r'^s03p01/(?P<fun>.*)/', S03p01Api.as_view()),

    url(r'^s03p02/(?P<fun>.*)/', S03p02Api.as_view()),

    url(r'^s04p01/(?P<fun>.*)/', S04p01Api.as_view()),

    url(r'^store_reg_api/(?P<fun>.*)/', StoreRegApi.as_view()),

    url(r'^menu_mgmt_api/(?P<fun>.*)/', MenuMgmtApi.as_view()),


    url(r'^ingredients_api/(?P<fun>.*)/', IngredientsApi.as_view()),

    url(r'^user_manager_api/(?P<fun>.*)/', UserManagerApi.as_view()),

    url(r'^user_api/(?P<fun>.*)/', UserApi.as_view()),

    url(r'^seat_manager_api/(?P<fun>.*)/', SeatManagerApi.as_view()),

    url(r'^setsubi_api/(?P<fun>.*)/', SetsubiApi.as_view()),

    url(r'^user_group_api/(?P<fun>.*)/', UserGroupApi.as_view()),

    url(r'^shop_cost_api/(?P<fun>.*)/', ShopCostApi.as_view()),

    url(r'^payment_api/(?P<fun>.*)/', PaymentApi.as_view()),

    url(r'^menu_upload_api/(?P<fun>.*)/', MenuUploadApi.as_view()),

    # takeout
    url(r'^takeout_api/(?P<fun>.*)/', TakeoutApi.as_view()),
    url(r'^takeout_order_api/(?P<fun>.*)/', TakeoutOrderApi.as_view()),
    url(r'^takeout_user_manager_api/(?P<fun>.*)/', TakeoutUserManagerApi.as_view()),
    url(r'^pay/(?P<fun>.*)/', PayApi.as_view()),
    url(r'^counter/(?P<fun>.*)/', CounterApi.as_view()),
    
]
urlpatterns += router.urls
