from rest_framework.serializers import SlugRelatedField


class CategoryRepresentation(SlugRelatedField):

    def to_representation(self, obj):
        data = super(CategoryRepresentation,
                     self).to_representation(obj)
        from .serializers import CategorySerializer
        data = CategorySerializer(obj).data
        return data


class GenreRepresentation(SlugRelatedField):

    def to_representation(self, obj):
        data = super(GenreRepresentation,
                     self).to_representation(obj)
        from .serializers import GenreSerializer
        data = GenreSerializer(obj).data
        return data
