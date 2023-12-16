from django.contrib import admin

from server.apps.user_request.models import Message, UserRequest


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin[Message]):
    """Сообщение."""

    list_display = (
        'id',
        'user_request',
        'message_type',
        'status',
    )
    list_filter = (
        'message_type',
        'status',
    )
    search_fields = (
        'user_request__user__email',
        'user_request__user__username',
        'user_request__user__first_name',
        'user_request__user__last_name',
    )
    ordering = (
        'id',
        'user_request',
        'message_type',
        'status',
    )
    raw_id_fields = (
        'user_request',
    )


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin[UserRequest]):
    """Запрос пользователя."""

    list_display = (
        'id',
        'project_sale_channel',
        'user',
        'client_id',
        'source_client_info',
        'status',
        'success_type',
    )
    list_filter = (
        'success_type',
        'status',
    )
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
    )
    ordering = (
        'id',
        'project_sale_channel',
        'user',
        'client_id',
        'source_client_info',
        'status',
        'success_type',
    )
    raw_id_fields = (
        'project_sale_channel',
        'user',
    )
