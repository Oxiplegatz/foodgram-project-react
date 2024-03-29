# Generated by Django 3.2.18 on 2023-04-04 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписки',
                'ordering': ('-subscribe_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='usersubscribe',
            constraint=models.UniqueConstraint(fields=('subscriber', 'author'), name='unique_subscription'),
        ),
    ]
