from django.urls import include, path
from rest_framework import routers
from .views import token_generate, signup_user, UsersViewSet


router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path(
        'v1/auth/token/',
        token_generate,
        name='token_generate'
    ),
    path('v1/auth/signup/', signup_user, name='signup'),
    path('v1/', include(router.urls)),
    
]
