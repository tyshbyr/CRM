from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            (request.user == obj.manager or request.user.is_staff)
        )
