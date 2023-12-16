import django_filters

from server.apps.llm_request.api.serializers import MessageSerializer
from server.apps.llm_request.models import Message
from server.apps.services.views import RetrieveListCreateViewSet


class MessageFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'marketing_text_request',
            'text',
            'message_type',
            'status',
        )


class MessageViewSet(RetrieveListCreateViewSet):
    """Сообщение."""

    serializer_class = MessageSerializer
    queryset = Message.objects.select_related('marketing_text_request')
    ordering_fields = '__all__'
    search_fields = (
        'text',
    )
    filterset_class = MessageFilter
