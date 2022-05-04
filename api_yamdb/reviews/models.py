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
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Slug категории', unique=True)
    description = models.TextField('Описание категории')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField('Наименование жанра', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)
    description = models.TextField('Описание жанра')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        'Наименование произведения',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField('Год произведения', db_index=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        db_index=True,
    )
    description = models.TextField('Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        through='GenreTitle',
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_category',
            ),
        ]
        ordering = ['year']


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_genre',
            ),
        ]
        ordering = ['genre']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
    )
    text = models.TextField('Текст обзора')
    author = models.ForeignKey(
        User,
        verbose_name='Автор обзора',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
    )
    score = models.IntegerField(
        'Оценка',
        default=None,
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
        ordering = ['pub_date']

    def __str__(self):
        return (
            f'Отзыв {self.author.first_name} {self.author.last_name}'
            f'на произведение {self.title.name}.'
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Обзор',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return (
            f'Комментарий {self.author.first_name} {self.author.last_name}'
            f'от {self.pub_date}.'
        )
