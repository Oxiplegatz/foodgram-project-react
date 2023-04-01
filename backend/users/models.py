from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserSubscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор',
    )
    subscribe_date = models.DateTimeField(
        'Дата подписки', auto_now_add=True
    )

    class Meta:
        ordering = ('-subscribe_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscription'
            ),
        ]
        verbose_name = 'Подписки'

    def __str__(self):
        return f'{str(self.subscriber)} подписан на {str(self.author)}'
