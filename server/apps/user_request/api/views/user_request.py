import django_filters
from rest_framework.decorators import action

from server.apps.services.views import RetrieveListCreateViewSet
from server.apps.user_request.api.serializers import UserRequestSerializer, \
    BaseMessageSerializer
from server.apps.user_request.api.serializers.user_request import (
    CreateUserRequestSerializer,
)
from server.apps.user_request.models import UserRequest, Message
from server.apps.user_request.services.user_reques import create_user_request


class UserRequestFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = UserRequest
        fields = (
            'id',
            'project_sale_channel',
            'user',
            'client_id',
            'source_client_info',
            'status',
            'success_type',
        )


class UserRequestViewSet(RetrieveListCreateViewSet):
    """Сообщение."""

    serializer_class = UserRequestSerializer
    create_serializer_class = CreateUserRequestSerializer
    queryset = UserRequest.objects.select_related(
        'project_sale_channel',
        'user',
    ).prefetch_related(
        'messages',
    )
    ordering_fields = '__all__'
    search_fields = (
        'client_id',
        'source_client_info',
    )
    filterset_class = UserRequestFilter
    permission_type_map = {
        **RetrieveListCreateViewSet.permission_type_map,
        'add_message': None,
    }

    def perform_create(self, serializer):
        serializer.instance = create_user_request(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )
