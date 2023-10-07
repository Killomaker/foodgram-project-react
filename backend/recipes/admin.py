from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка тэгов"""

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка ингридентов"""

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientAmountInline(admin.TabularInline):
    """Класс добавления ингридиентов"""

    model = IngredientAmount
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка рецптов"""

    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        IngredientAmountInline,
    ]

    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author', 'name')

    def get_ingredients(self, object):
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    def get_tags(self, object):
        return '\n'.join((tag.name for tag in object.tags.all()))

    def count_favorite(self, object):
        return object.favoriting.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)
