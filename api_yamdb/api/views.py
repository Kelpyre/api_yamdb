from rest_framework import viewsets, mixins, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, TitlePostPatchSerializer
)


class CreateRetrieveDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Category, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Genre, slug=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleSerializer
        return TitlePostPatchSerializer
