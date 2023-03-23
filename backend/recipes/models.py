from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        null=False,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_combo'
            ),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        null=False,
        blank=False,
        unique=True
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        null=False,
        blank=False,
        unique=True
    )
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        null=False,
        blank=False
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(
        upload_to='recipes/',
        null=False,
        blank=False
    )
    text = models.TextField('Описание рецепта', null=False, blank=False)
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
