from django.contrib import admin

from server.apps.llm_request.models import Message, RequestData


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin[Message]):
    """Сообщение."""

    list_display = (
        'id',
        'request_data',
        'message_type',
        'status',
    )
    list_filter = (
        'message_type',
        'status',
    )
    search_fields = (
        'request_data__user__email',
        'request_data__user__username',
        'request_data__user__first_name',
        'request_data__user__last_name',
    )
    ordering = (
        'id',
        'request_data',
        'message_type',
        'status',
    )
    raw_id_fields = (
        'request_data',
    )


@admin.register(RequestData)
class RequestDataAdmin(admin.ModelAdmin[RequestData]):
    """Данные для запроса."""

    list_display = (
        'id',
        'project_sale_channel',
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
        'project_sale_channel__project__name',
        'project_sale_channel__sale_channel__name',
    )
    ordering = (
        'id',
        'project_sale_channel',
        'client_id',
        'source_client_info',
        'status',
        'success_type',
    )
    raw_id_fields = (
        'project_sale_channel',
    )
