from rest_framework import serializers

from users.models import User


class SignupUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254, required=True)
    email = serializers.EmailField(max_length=150, required=True)
    
    # class Meta:
    #     fields = ('email', 'username',)

    def validate_username(self, username):
        if str.lower(username) == 'me':
            raise serializers.ValidationError(
                'Имя ""me"" запрещено'
            )
        return username


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

    def validate_username(self, username):
        if str.lower(username) == 'me':
            raise serializers.ValidationError(
                'Имя ""me"" запрещено'
            )
        return username


class UserMeSerializer(UsersSerializer):
    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

        read_only_fields = ('role',)
        model = User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
