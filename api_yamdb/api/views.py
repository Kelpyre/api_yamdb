import uuid

from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Comment, Review, Title
from .permissions import AdminOnly, AuthorAdminModeratorOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    LoginSerializer,
    SignupUserSerializer,
    UserMeSerializer,
    UsersSerializer
)
from users.models import User
from users.send_mail_util import send_password_mail


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    """Регистрация юзера и получение кода для api"""
    serializer = SignupUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        obj_user, created = User.objects.get_or_create(
            email=email,
            username=username
        )
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    generate_uuid = str(uuid.uuid4())
    obj_user.confirmation_code = generate_uuid
    obj_user.save()
    send_password_mail(email, generate_uuid)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Управление пользователями"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated, AdminOnly)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username')
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,))
    def administration_user_me(self, request):
        get_me_user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(get_me_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(
            get_me_user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_generate(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data['username']
    get_user = get_object_or_404(User, username=username)
    if confirmation_code == get_user.confirmation_code:
        token = str(AccessToken.for_user(get_user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
