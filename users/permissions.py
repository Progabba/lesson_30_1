from rest_framework import permissions

class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moder").exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if obj.user == request.user:
            return True
        return False

