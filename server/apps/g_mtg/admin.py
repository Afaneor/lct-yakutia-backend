from django.contrib import admin

from server.apps.g_mtg.models import Product, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    list_filter = ('user', 'product', 'name', 'description', 'prompt')
    search_fields = ('user', 'product', 'name', 'description', 'prompt')
    list_display = ('user', 'product', 'name', 'description', 'prompt')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    """Продукт банка."""

    list_filter = ('name', 'description')
    search_fields = ('name', 'description')
    list_display = ('name', 'description')
