from django.shortcuts import render
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from master.models.guest import Guest, GuestDevice, GuestUser
from master.serializer.guest import GuestSerializer
from common.cache.application import Application
# Create your views here.

from django.views.decorators.cache import cache_page
import channels.layers
from asgiref.sync import async_to_sync
import common.saas as saas


@api_view(['GET', 'POST'])
# @cache_page(60 * 15)
def list(request):
    """
    List all code snippets, or create a new snippet.
    """

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        saas.group_name(saas.id(request), 'chat_aaa'),
        {
            'type': 'chat_message',
            'message': "AAAAAAAAAAAAAAAAAAAAAAA"
        })

    count = Application.get_count()
    print(count)
    count += 1
    Application.set_count(count)
    if request.method == 'GET':
        guest = Guest.objects.get(id=1)
        serializer = GuestSerializer(instance=guest)

        return Response(serializer.data)
