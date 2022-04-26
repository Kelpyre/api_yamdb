from rest_framework import serializers
from users.models import User


class CreateUserserializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username',)
        model = User