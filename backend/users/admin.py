from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс настройки пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_admin'
    )
    list_editable = ('is_admin',)
    list_filter = ('username', 'email')
    search_fields = ('username',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Класс настройки подписок."""

    list_display = (
        'pk',
        'author',
        'subscriber',
    )

    list_editable = ('author', 'subscriber')
    list_filter = ('author',)
    search_fields = ('author',)
