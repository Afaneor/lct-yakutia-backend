from typing import List, Dict, Any

import django_filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.g_mtg.api.serializers import ProjectSaleChannelSerializer, \
    UploadDataSerializer
from server.apps.g_mtg.models import ProjectSaleChannel
from server.apps.services.views import BaseReadOnlyViewSet
import pylightxl as xl

from server.apps.user_request.services.user_reques import \
    validate_client_data_decoding, create_user_request
from django.utils.translation import gettext_lazy as _


class ProjectSaleChannelFilter(django_filters.FilterSet):
    """Фильтр для клиента."""

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'project',
            'sale_channel',
        )


class ProjectSaleChannelViewSet(BaseReadOnlyViewSet):
    """Продукт банка."""

    serializer_class = ProjectSaleChannelSerializer
    queryset = ProjectSaleChannel.objects.all()
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProjectSaleChannelFilter
    permission_type_map = {
        **BaseReadOnlyViewSet.permission_type_map,
        'add_client': None,
    }

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client',
        detail=True,
        serializer_class=UploadDataSerializer,
    )
    def add_client(self, request: Request, pk: int):
        """Загрузка данных по клиенты."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with request.FILES['file'].open(mode='r') as file:
            db = xl.readxl(file)
            file_data: List[Dict[str, Any]] = []
            file_header: List[Any] = []
            for list_name in db.ws_names:
                for index, row in enumerate(db.ws(ws=list_name).rows):
                    if index != 0:
                        file_data.append(dict(zip(file_header, row)))
                    else:
                        file_header = row

        client_data_decoding = serializer.validated_data['client_data_decoding']
        validate_client_data_decoding(
            client_data_decoding=client_data_decoding,
            file_header=file_header,
        )

        create_user_request(
            project_sale_channel=self.get_object(),
            user=self.request.user,
            file_name=request.FILES['file'].name,
            all_client_data=file_data,
            client_data_decoding=client_data_decoding,
        )

        return Response(
            data={'detail': _('Данные загружены')},
            status=status.HTTP_201_CREATED
        )

