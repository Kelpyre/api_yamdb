from statistics import mean
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from .validators import validate_year
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(validators=[validate_year])

    class Meta(object):
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def get_rating(self, obj):
        scores = Review.objects.filter(title=obj.id).values_list(
            'score', flat=True)
        if scores:
            rating = mean(scores)
            return rating
        return None


class TitlePostPatchSerializer(TitleSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    def to_representation(self, instance):
        data = super(TitlePostPatchSerializer,
                     self).to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data
        data['genre'] = []
        for entry in instance.genre.all():
            genre = GenreSerializer(entry).data
            data['genre'].append(genre)
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        author = self.context['request'].user
        review_exists = Review.objects.filter(
            author=author,
            title=title
        ).exists()
        if review_exists and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение !')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


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
