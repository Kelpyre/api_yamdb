from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
REVIEW_SCORE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        default=1,
        choices=REVIEW_SCORE,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author',
            ),
        ]

    def __str__(self):
        return (
            f'Отзыв {self.author.first_name} {self.author.last_name}'
            f'на произведение {self.title.name}.'
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return (
            f'Комментарий {self.author.first_name} {self.author.last_name}'
            f'от {self.pub_date}.'
        )
