from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CommentViewSet, ReviewViewSet, token_generate, signup_user, UsersViewSet

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
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
