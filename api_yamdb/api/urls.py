from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
