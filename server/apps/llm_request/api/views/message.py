import django_filters

from server.apps.llm_request.api.serializers import (
    CreateMessageSerializer,
    MessageSerializer,
    UpdateMessageSerializer,
)
from server.apps.llm_request.models import Message
from server.apps.llm_request.services.message import create_message
from server.apps.services.views import (
    BaseModelViewSet,
    RetrieveListCreateUpdateViewSet,
)


class MessageFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'request_data',
            'parent',
            'user',
            'text',
            'message_type',
            'status',
        )


class MessageViewSet(RetrieveListCreateUpdateViewSet):
    """Сообщение."""

    serializer_class = MessageSerializer
    create_serializer_class = CreateMessageSerializer
    update_serializer_class = UpdateMessageSerializer
    queryset = Message.objects.select_related(
        'request_data',
        'parent',
        'user',
    )
    ordering_fields = '__all__'
    search_fields = (
        'text',
    )
    filterset_class = MessageFilter

    def perform_create(self, serializer):
        """Создать сообщение."""
        serializer.instance = create_message(
            validated_data=serializer.validated_data,
            user=self.request.user,
        )
