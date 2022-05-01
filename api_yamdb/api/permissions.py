from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnly(BasePermission):
    """Доступ только у админа или суперюзера"""
    def has_permission(self, request, view):
        return(request.user.is_admin)


class AuthorOrAdministration(BasePermission):
    """Доступ у автора или админа, модератора"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )
