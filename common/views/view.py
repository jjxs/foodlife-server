from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from urllib.parse import urlparse
from datetime import datetime, date

from django.core.exceptions import ValidationError
from common.permission.controller import UserRoleAuthenticated
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404 as _get_list_or_404

import json
import ast



def json_supporter(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(repr(obj) + "cannot seriializable")


class MultipleModelViewSet(viewsets.ModelViewSet):
    """
    Create a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        print("################# update ########################")
        if isinstance(request.data, list):
            pks = [ data["id"] for data in request.data]
            instances = self.get_object_list(pks)            

            # TODO: 此处没有考虑事务问题，以后补充
            for instance, data in zip(instances, request.data):
                serializer = self.get_serializer(instance, data=data, partial=partial) 
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)     

        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        
        

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object_list(self, pks):

        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {'id__in': pks}

        try:
            obj_list = queryset.filter(**filter_kwargs)
            if not obj_list:
                raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)

        except (TypeError, ValueError, ValidationError):
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj_list)

        return obj_list

    def destroy(self, request, *args, **kwargs):

        if "pk" in kwargs and "," in kwargs["pk"]:
            pks = ast.literal_eval(kwargs["pk"])
            instance = self.get_object_list(pks)
        else:
            instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SampleAPIView(APIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def to_json(self, obj):
        return json.dumps(obj, default=json_supporter)
        # Note: Views are made CSRF exempt from within `as_view` as to prevent
        # accidental removal of this exemption in cases where `dispatch` needs to
        # be overridden.

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        querys = request.query_params
        data = request.data

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), None)
                fun_name = self.kwargs.get('fun')
                if not handler and fun_name:
                    handler = getattr(self, str(fun_name).lower(),
                                      self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request,  *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)
        return self.response
