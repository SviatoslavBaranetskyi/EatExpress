from rest_framework.permissions import BasePermission


class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Couriers').exists()
