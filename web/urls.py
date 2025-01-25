"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from django.http import HttpResponse

urlpatterns = [


    # #app.human
    # #Djangoの画面を上書き
    # url(r'^admin/human/', include('human.url.index')),
    # url(r'^human/', include('human.url.index')),

    # #app.manger
    # #Djangoの画面を上書き
    # url(r'^admin/manager/', include('manager.url.index')),
    # url(r'^manager/', include('manager.url.index')),

    # url(r'^custom/', include('custom.url.index')),
    # url(r'^shop/', include('shop.url.index')),
    # #url(r'',include('shop.url.index')),
    url(r'^test/', lambda request: HttpResponse(''), name='test'),
    url(r'^restaurant/', include('restaurant.urls')),
    url(r'^master/', include('master.urls')),
    url(r'^guest/', include('guest.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login', obtain_jwt_token),
    url(r'^(store|s)/', include('app_store.urls'))
]
