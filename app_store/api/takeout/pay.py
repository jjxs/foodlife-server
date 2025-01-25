
import datetime
from zipfile import is_zipfile

from botocore import model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import (Takeout, TakeoutOrder)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, serializers
import paypayopa
from django.shortcuts import redirect

class PayApi(BaseAPI):
    permission_classes = (permissions.AllowAny,)

    def order(self, request, params):
        client = paypayopa.Client(auth=("m_aw0Lec3aih_SG2b", "94VhFqDC3ov0gdOAl9fBOkxfGAXDdxbqGOwhLac9"), production_mode=False) #Set True for Production Environment. By Default this is set False for Sandbox Environment.
        client.set_assume_merchant("MERCHANT_ID")

        # Creating the payload to create a QR Code, additional parameters can be added basis the API Documentation
        merchantPaymentId = 7
        request = {
            "merchantPaymentId": merchantPaymentId,
            "codeType": "ORDER_QR",
            "redirectUrl":"http://foobar.com",
            "redirectType":"WEB_LINK",
            "orderDescription":"Mune's Favourite Cake",
            "amount": {
                "amount": 1 ,
                "currency": "JPY"
            },
            "orderItems": []
        }
        # Calling the method to create a qr code
        response = client.code.create_qr_code(request)
        # Printing if the method call was SUCCESS
        print(response)
        if "resultInfo" in response and "code" in response["resultInfo"]:
            if response["resultInfo"]["code"] == "SUCCESS":
                redirect_url = response["data"]["url"]
                return redirect(redirect_url)

        return JsonResponse(result=True, data=response)

    def history(self, request, params):
        # get takeout order history by user
        result = []
        return JsonResponse(result=True, data=result)