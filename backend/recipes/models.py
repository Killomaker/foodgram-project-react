from colorfield.fields import ColorField
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models

from rest_framework import serializers

from backend.settings import LENGTH_TEXT, TEXT_LENGTH_150
from users.models import User


class Tag(models.Model):
    """Класс тегов."""

    name = models.CharField(
        max_length=50,
        verbose_name='Hазвание',
        unique=True,
        db_index=True
    )

    color = ColorField(
        default='#FF0000',
        max_length=7,
        verbose_name='цвет',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг тега содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.slug[:LENGTH_TEXT]


class Ingredient(models.Model):
    """Класс ингредиентов."""

    name = models.CharField(
        max_length=TEXT_LENGTH_150,
        verbose_name='Hазвание',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=5,
        verbose_name='единица измерения'
    )

    def validate_ingredients(self, ingredients):
        """Проверяем, что рецепт содержит уникальные ингредиенты"""
        ingredients_data = [
            ingredient.get('id') for ingredient in ingredients
        ]
        if len(ingredients_data) != len(set(ingredients_data)):
            raise serializers.ValidationError(
                'Ингредиенты рецепта должны быть уникальными'
            )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Recipe(models.Model):
    """Класс рецептов."""

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='ингредиенты'

    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='изображение'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Hазвание',
        db_index=True
    )
    text = models.TextField(verbose_name='описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления(мин.)',
        validators=[
            MinValueValidator(
                0,
                message='Время приготовления не может быть меньше 0'
            ),
            MaxValueValidator(
                1000,
                message='Количество ингредиента не может быть больше 1000'
            )
        ],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class IngredientAmount(models.Model):
    """Вспомогательный класс, связывающий рецепты и ингредиенты."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиента не может быть нулевым'
            ),
            MaxValueValidator(
                1000,
                message='Количество ингредиента не может быть больше тысячи'
            )
        ],
    )

    class Meta:
        verbose_name = 'Соответствие ингредиента и рецепта'
        verbose_name_plural = 'Таблица соответствия ингредиентов и рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.recipe} содержит ингредиент/ты {self.ingredient}'


class FavoriteAndShoppingCartAbstractModel(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        abstract = True


class Favorite(FavoriteAndShoppingCartAbstractModel):
    """Довавление рецептов в избранное."""

    recipe = models.ForeignKey(
        Recipe,
        related_name='favoriting',
    )
    user = models.ForeignKey(
        User,
        related_name='favoriting',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(FavoriteAndShoppingCartAbstractModel):
    """Класс для составления списка покупок."""

    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Рецепт пользователя для списка покупок'
        verbose_name_plural = 'Рецепты пользователей для списка покупок'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
