from rest_framework import permissions

class isOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return str(obj.user) == str(request.user)