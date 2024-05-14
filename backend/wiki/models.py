from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    email = models.CharField(
        max_length=150,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Enter a valid slug',
                code='invalid_slug'
            )
        ],
        unique=True,
        verbose_name='Уникальный юзернейм'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150, verbose_name='Пароль')

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',]
    USERNAME_FIELD = 'username'


class Wiki(models.Model):
    title = models.CharField(
        max_length=254,
        verbose_name='Заголовок'
    )
    image = models.ImageField(
        upload_to='wiki',
        verbose_name='Фотография'
    )
    text = models.TextField(
        verbose_name='Описаниe'
    )
    author = models.ForeignKey(
        CustomUser, verbose_name='Автор',
        related_name='wiki_all',
        on_delete=models.CASCADE
    )


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='author',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    subscribe = models.ForeignKey(
        CustomUser, related_name='subscribe',
        verbose_name='Посписчик',
        on_delete=models.CASCADE
    )


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Поставил лайк',
        on_delete=models.CASCADE,
        related_name='user_likes'
    )
    wiki_like = models.ForeignKey(
        Wiki,
        verbose_name='Лайкнутая статья',
        on_delete=models.CASCADE,
        related_name='wiki_likes'
    )


class Dislike(models.Model):
    user_diser = models.ForeignKey(
        CustomUser,
        verbose_name='Поставил дислайк',
        on_delete=models.CASCADE,
        related_name='user_dislikes'
    )
    wiki_dislike = models.ForeignKey(
        Wiki,
        verbose_name='Дислайкнутая статья',
        on_delete=models.CASCADE,
        related_name='wiki_dislikes'
    )
