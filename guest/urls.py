from django.conf.urls import url
from .controller.guest import GuestController, GuestDataController
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'data', GuestDataController)
router.register(r'guest', GuestController)
urlpatterns = [
]
urlpatterns += router.urls
