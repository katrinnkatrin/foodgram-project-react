from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (request.method == 'POST' or request.user.is_superuser
               or (obj.author == request.user)):
                return True
        return request.method in SAFE_METHODS
