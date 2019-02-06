from rest_framework import permissions


class IsObjectOwner(permissions.BasePermission):

    message = "This resource does not belong to you. You do not have \
               permissions to edit or delete"

    def has_object_permission(self, request, view, obj):
        # Grants users permissions for read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Grants user permission to edit or delete object if they're the user
        return obj.user == request.user
