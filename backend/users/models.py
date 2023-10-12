from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from backend.settings import(
    LENGTH_TEXT,
    TEXT_LENGTH_150,
    TEXT_LENGTH_254
)

class User(AbstractUser):
    email = models.EmailField(
        max_length=TEXT_LENGTH_254,
        verbose_name='email',
        unique=True,
        db_index=True
    )
    username = models.CharField(
        max_length=TEXT_LENGTH_150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    first_name = models.CharField(
        max_length=TEXT_LENGTH_150,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=TEXT_LENGTH_150,
        verbose_name='фамилия'
    )
    password = models.CharField(
        max_length=TEXT_LENGTH_150,
        verbose_name='пароль'
    )
    is_admin = models.BooleanField(
        verbose_name='администратор',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:LENGTH_TEXT]


class Subscription(models.Model):
    """Класс для подписок."""

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        )

    def __str__(self):
        return f'{self.subscriber} подписан на: {self.author}'
