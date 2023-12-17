import django_filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.llm_request.api.serializers import (
    CreateMessageSerializer,
    MessageSerializer,
    UpdateMessageSerializer, MultipleCreationMessagesSerializer,
)
from server.apps.llm_request.models import Message
from django.utils.translation import gettext_lazy as _
from server.apps.llm_request.services.message import create_message, \
    multiple_creation_request_data
from server.apps.services.views import (
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
    permission_type_map = {
        **RetrieveListCreateUpdateViewSet.permission_type_map,
        'multiple_creation': 'list',
    }

    def perform_create(self, serializer):
        """Создать сообщение."""
        serializer.instance = create_message(
            validated_data=serializer.validated_data,
            user=self.request.user,
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path='multiple-creation',
        serializer_class=MultipleCreationMessagesSerializer,
    )
    def multiple_creation(self, request: Request):
        """Множественное создание сообщений."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        multiple_creation_request_data(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            data={'detail': _('Данные отправлены, ожидайте ответа')},
            status=status.HTTP_200_OK,
        )
