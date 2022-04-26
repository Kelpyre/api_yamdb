from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CreateUserViewSet


router = routers.DefaultRouter()
router.register('auth/signup', CreateUserViewSet, basename='signup')

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/', include(router.urls)),
]
