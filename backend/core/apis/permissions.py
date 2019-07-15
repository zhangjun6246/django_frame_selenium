# -*- coding: utf-8 -*-

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class UserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return True
