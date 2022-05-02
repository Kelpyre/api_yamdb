from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review
from .validators import validate_year


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
            rating = sum(scores)
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
