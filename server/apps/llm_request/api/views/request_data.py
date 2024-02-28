import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.llm_request.api.serializers import (
    CreateRequestDataSerializer,
    ListRequestDataSerializer,
    MultipleCreationRawRequestDataSerializer,
    MultipleCreationRequestDataSerializer,
    RequestDataSerializer,
    UpdateRequestDataSerializer,
)
from server.apps.llm_request.models import RequestData
from server.apps.llm_request.services.request_data import (
    create_request_data,
    multiple_creation_request_data,
    raw_multiple_creation_request_data,
)
from server.apps.services.views import RetrieveListCreateUpdateViewSet


class RequestDataFilter(django_filters.FilterSet):
    """Фильтр данных для запроса."""

    class Meta(object):
        model = RequestData
        fields = (
            'id',
            'project_sale_channel',
            'client_id',
            'source_client_info',
            'status',
            'success_type',
        )


class RequestDataViewSet(RetrieveListCreateUpdateViewSet):
    """Данные для запроса."""

    serializer_class = RequestDataSerializer
    list_serializer_class = ListRequestDataSerializer
    create_serializer_class = CreateRequestDataSerializer
    update_serializer_class = UpdateRequestDataSerializer
    queryset = RequestData.objects.select_related(
        'project_sale_channel',
    ).prefetch_related(
        'messages',
    )
    ordering_fields = '__all__'
    search_fields = (
        'client_id',
        'source_client_info',
    )
    filterset_class = RequestDataFilter
    permission_type_map = {
        **RetrieveListCreateUpdateViewSet.permission_type_map,
        'add_message': None,
    }

    def perform_create(self, serializer):
        serializer.instance = create_request_data(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path='multiple-creation',
        serializer_class=MultipleCreationRequestDataSerializer,
    )
    def multiple_creation(self, request: Request):
        """Множественное создание данных для запросов."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        multiple_creation_request_data(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            data={'detail': _('Данные отправлены, ожидайте ответа')},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path='raw-multiple-creation',
        serializer_class=MultipleCreationRawRequestDataSerializer,
    )
    def raw_multiple_creation(self, request: Request):
        """Множественное создание сырых данных для запросов."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = raw_multiple_creation_request_data(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            data=response,
            status=status.HTTP_200_OK,
        )
