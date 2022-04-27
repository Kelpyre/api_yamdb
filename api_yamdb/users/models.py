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
