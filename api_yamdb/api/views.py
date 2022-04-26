from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from users.models import User
from .serializers import CreateUserserializer


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserserializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)