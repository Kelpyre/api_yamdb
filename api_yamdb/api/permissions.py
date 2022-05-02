from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnly(BasePermission):
    """Доступ только у админа или суперюзера"""

    def has_permission(self, request, view):
        return(request.user.is_admin)


class AuthorAdminModeratorOrReadOnly(BasePermission):
    message = 'Изменение или удаление чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class CategoryGenreTitle(BasePermission):
    message = 'Нет прав на создание объекта!'

    def has_permission(self, request, view):
        return(
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
                )
        )


class ReviewComment(BasePermission):
    message = 'Изменение или удаление чужого контента запрещено!'

    def has_permission(self, request, view):
        return(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
            )
        return(request.method in SAFE_METHODS)
