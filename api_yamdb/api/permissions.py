from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

class AdminOnly(permissions.BasePermission):
    pass