from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )
    role = models.CharField(
        max_length=50,
        default='user',
        choices=USER_ROLES
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=False,
        blank=False
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.username)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


CustomUser._meta.get_field('username').max_length = 150
CustomUser._meta.get_field('email').max_length = 254
CustomUser._meta.get_field('email')._unique = True
