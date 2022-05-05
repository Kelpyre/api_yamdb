from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, CommentViewSet,
    ReviewViewSet, token_generate,
    signup_user, UsersViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path(
        'v1/auth/token/',
        token_generate,
        name='token_generate'
    ),
    path('v1/auth/signup/', signup_user, name='signup'),
    path('v1/', include(router.urls)),
    ]
