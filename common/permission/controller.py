from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import BasePermission
from django.core.cache import cache
from master.data.cache_data import get_role_auth


class UserRoleAuthenticated(BasePermission):

    def has_permission(self, request, view):
        print("has_permission")
        try:
            getattr(request, "role")
        except AttributeError:
            return False
        print(request.user.id)
        roles = get_role_auth(request.role)
        
        # #テストのため
        # return True
        if request.user.id!=None:
            return True
        else:
            return False

        # for viewname in roles:
        #     if viewname in str(view):
        #         if 'ALLOW' in roles.get(viewname):
        #             # すべて許可される場合
        #             return True
        #         elif request.method in roles.get(viewname):
        #             return True
        #         else:
        #             continue

        # return False
