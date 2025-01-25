from django.conf.urls import url
from restaurant import views
from restaurant.controller.seat import *  # SeatStatusController, seat_start
from restaurant.controller.menu import *
from restaurant.controller.charts import *
from restaurant.controller.master import *
from restaurant.controller.order import *
from restaurant.controller.kitchen import *
from restaurant.controller.counter import *
from restaurant.controller.menutop3 import *
from restaurant.controller.reserve import *

from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    # url(r'^seat_start', seat_start),
    url(r'^seat_status', SeatStatusController.as_view()),
    url(r'^seat_list', SeatListController.as_view()),
    url(r'^list/$', views.list),
    url(r'^menu/(?P<fun>.*)/', MenuController.as_view()),
    url(r'^charts/(?P<fun>.*)/', ChartsController.as_view()),
    url(r'^master/(?P<fun>.*)/', MasterController.as_view()),
    url(r'^order/(?P<fun>.*)/', OrderController.as_view()),
    url(r'^order_history/(?P<fun>.*)/', OrderHistoryController.as_view()),
    url(r'^order_list/(?P<fun>.*)/', OrderListController.as_view()),
    url(r'^kitchen/(?P<fun>.*)/', KitchenController.as_view()),
    url(r'^counter/(?P<fun>.*)/', CounterController.as_view()),
    url(r'^seat/(?P<fun>.*)/', SeatController.as_view()),
    url(r'^menutop3/(?P<fun>.*)/', MenuTop3Controller.as_view()),
    url(r'^reserve/(?P<fun>.*)/', ReserveController.as_view()),
    url(r'^reserve_client/(?P<fun>.*)/', ReserveClientController.as_view()),

]
urlpatterns += router.urls
