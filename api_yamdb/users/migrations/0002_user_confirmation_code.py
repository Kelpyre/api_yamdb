# Generated by Django 2.2.16 on 2022-04-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.TextField(blank=True, null=True, verbose_name='Пароль для api'),
        ),
    ]
