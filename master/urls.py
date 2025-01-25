from django.conf.urls import url
from rest_framework import routers
from master.controller.common import *
from master.controller.master import *
from master.controller.seat import *
from master.controller.menu import *
from master.controller.order import *

router = routers.DefaultRouter()
router.register(r'seatgroup', SeatGroupController)
router.register(r'seat', SeatController)
router.register(r'master', MasterController)
router.register(r'masterdata', MasterDataController)
router.register(r'masterdatagroup', MasterDataGroupController)
router.register(r'menu', MenuController)
router.register(r'menucategory', MenuCategoryController)
router.register(r'menufree', MenuFreeController)
#router.register(r'menufreedetail', MenuFreeDetailController)
router.register(r'seatstatus', SeatStatusController)
router.register(r'order', OrderController)
urlpatterns = [
    # url(r'^master', MasterController.as_view()),
    url(r'^init', InitController.as_view()),
    url(r'^app', AppController.as_view()),
    url(r'^qr/(?P<fun>.*)/', QRController.as_view()),
    # 
]
urlpatterns += router.urls
