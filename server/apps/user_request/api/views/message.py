import django_filters

from server.apps.services.views import RetrieveListCreateViewSet
from server.apps.user_request.api.serializers import MessageSerializer
from server.apps.user_request.models import Message


class MessageFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'user_request',
            'text',
            'message_type',
            'status',
        )


class MessageViewSet(RetrieveListCreateViewSet):
    """Сообщение."""

    serializer_class = MessageSerializer
    queryset = Message.objects.select_related('user_request')
    ordering_fields = '__all__'
    search_fields = (
        'text',
    )
    filterset_class = MessageFilter
