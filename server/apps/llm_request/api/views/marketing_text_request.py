import django_filters
from rest_framework.decorators import action
from rest_framework.request import Request

from server.apps.llm_request.api.serializers import (
    BaseMessageSerializer,
    MarketingTextRequestSerializer,
)
from server.apps.llm_request.api.serializers.marketing_text_request import (
    CreateMarketingTextRequestSerializer,
)
from server.apps.llm_request.models import MarketingTextRequest, Message
from server.apps.llm_request.services.user_reques import create_user_request
from server.apps.llm_request.tasks import send_request_for_get_channel_advice
from server.apps.services.views import RetrieveListCreateViewSet


class MarketingTextRequestFilter(django_filters.FilterSet):
    """Фильтр для сообщений."""

    class Meta(object):
        model = MarketingTextRequest
        fields = (
            'id',
            'project_sale_channel',
            'user',
            'client_id',
            'source_client_info',
            'status',
            'success_type',
        )


class MarketingTextRequestViewSet(RetrieveListCreateViewSet):
    """Сообщение."""

    serializer_class = MarketingTextRequestSerializer
    create_serializer_class = CreateMarketingTextRequestSerializer
    queryset = MarketingTextRequest.objects.select_related(
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
    filterset_class = MarketingTextRequestFilter
    permission_type_map = {
        **RetrieveListCreateViewSet.permission_type_map,
        'add_message': None,
    }

    def perform_create(self, serializer):
        serializer.instance = create_user_request(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

    @action(
        ['POST'],
        detail=True,
        url_path='get-channel-advice',
    )
    def get_channel_advice(self, request: Request, pk: int):
        """Получить совет по выбору канала."""
        marketing_text_request = self.get_object()
        prompt = marketing_text_request.client_data
        send_request_for_get_channel_advice.apply_async(
            kwargs={
                'prompt': prompt,
                'user_request_id': marketing_text_request.id,
            }
        )

        return Response(
            data={'detail': _('Пользователь успешно вышел из системы')},
            status=status.HTTP_200_OK,
        )
