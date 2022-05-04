# Generated by Django 2.2.16 on 2022-05-04 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220503_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['pub_date']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='genretitle',
            options={'ordering': ['genre']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['year']},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(verbose_name='Описание категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Имя категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug категории'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Обзор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(verbose_name='Описание жанра'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование жанра'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug жанра'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор обзора'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=None, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст обзора'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(verbose_name='Описание произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(db_index=True, through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(db_index=True, max_length=256, verbose_name='Наименование произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(db_index=True, verbose_name='Год произведения'),
        ),
    ]
