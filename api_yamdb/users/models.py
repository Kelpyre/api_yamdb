from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        default='user',
        choices=USER_ROLES,
        max_length=55,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=155,
        null=True
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
