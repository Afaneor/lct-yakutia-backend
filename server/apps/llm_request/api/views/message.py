import django_filters
from requests import Request
from rest_framework.decorators import action

from server.apps.llm_request.api.serializers import (
    CreateMessageSerializer,
    MessageSerializer,
    UpdateMessageSerializer,
)
from server.apps.llm_request.models import Message
from server.apps.llm_request.services.message import create_message
from server.apps.services.views import RetrieveListCreateUpdateViewSet
from server.apps.llm_request.tasks import send_request_for_get_channel_advice


class MessageFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = Message
        fields = (
            'id',
            'request_data',
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
        'request_datat',
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

    # FIXME доделать
    @action(
        methods=['POST'],
        detail=False,
        url_path='get-channel-advice',
    )
    def get_channel_advice(self, request: Request):
        """Получить совет по выбору канала."""
        request_data = self.get_object()
        prompt = request_data.client_data
        send_request_for_get_channel_advice.apply_async(
            kwargs={
                'prompt': prompt,
                'request_data_id': request_data.id,
            }
        )

        return Response(
            data={'detail': _('Пользователь успешно вышел из системы')},
            status=status.HTTP_200_OK,
        )
