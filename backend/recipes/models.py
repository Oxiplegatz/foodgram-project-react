from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Единица измерения'
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
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=False,
        blank=False,
        verbose_name='Картинка'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления (в минутах)'
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=f'Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Список ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            ),
        ]

    def __str__(self):
        return f'Ингредиент для рецепта {self.recipe.name}'


class RecipeFavorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            ),
        ]

    def __str__(self):
        return f'В избранном: {str(self.recipe)}'


class RecipeInCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_in_cart'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_in_cart'
            ),
        ]

    def __str__(self):
        return f'В списке покупок: {str(self.recipe)}'
