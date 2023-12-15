from django.contrib import admin

from server.apps.g_mtg.models import (
    Product,
    Project,
    ProjectSaleChannel,
    ProjectUser,
    SaleChannel,
)


@admin.register(SaleChannel)
class SaleChannelAdmin(admin.ModelAdmin[SaleChannel]):
    """Канал продаж."""

    list_display = (
        'id',
        'name',
        'key_name',
    )
    list_filter = (
        'key_name',
        'projects__product',
    )
    search_fields = (
        'name',
        'key_name',
        'description',
        'projects',
        'projects__name',
        'projects__product',
        'projects__product__name',
    )
    ordering = (
        'id',
        'name',
        'key_name',
    )


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin[ProjectUser]):
    """Пользователь проекта."""

    list_display = (
        'id',
        'project',
        'user',
        'role',
    )
    list_filter = (
        'project__product',
        'role',
    )
    search_fields = (
        'project__name',
        'project__product__name',
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'role',
    )
    ordering = (
        'id',
        'project',
        'user',
        'role',
    )


@admin.register(ProjectSaleChannel)
class ProjectSaleChannelAdmin(admin.ModelAdmin[ProjectSaleChannel]):
    """Канал продаж в рамках проекта."""

    list_display = (
        'id',
        'project',
        'sale_channel',
    )
    list_filter = (
        'project__product',
        'sale_channel',
    )
    search_fields = (
        'project__name',
        'project__product__name',
        'sale_channel__name',
        'sale_channel__key_name',
    )
    ordering = (
        'id',
        'project',
        'sale_channel',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    list_display = (
        'id',
        'product',
        'name',
    )
    list_filter = (
        'product',
        'sales_channels',
    )
    search_fields = (
        'name',
        'product__name',
        'sales_channels__name',
        'sales_channels__key_name',
    )
    ordering = (
        'id',
        'product',
        'name',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    """Продукт банка."""

    list_display = (
        'id',
        'name',
        'key_name',
    )
    list_filter = (
        'key_name',
    )
    search_fields = (
        'name',
        'key_name',
    )
    ordering = (
        'id',
        'name',
        'key_name',
    )
