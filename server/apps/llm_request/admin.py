from django.contrib import admin

from server.apps.llm_request.models import MarketingTextRequest, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin[Message]):
    """Сообщение."""

    list_display = (
        'id',
        'marketing_text_request',
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
        'marketing_text_request',
        'message_type',
        'status',
    )
    raw_id_fields = (
        'marketing_text_request',
    )


@admin.register(MarketingTextRequest)
class MarketingTextRequestAdmin(admin.ModelAdmin[MarketingTextRequest]):
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
