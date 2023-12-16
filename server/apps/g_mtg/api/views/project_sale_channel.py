from typing import Any, Dict, List

import django_filters
import psycopg2
import pylightxl as xl
from django.utils.translation import gettext_lazy as _
from pymongo import MongoClient
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.g_mtg.api.serializers import (
    MultipleCreateProjectSaleChannelSerializer,
    ProjectSaleChannelSerializer,
    UploadDataFromFileSerializer, UploadDataFromPostgresSerializer,
    UploadDataFromMongoSerializer, UpdateProjectSaleChannelSerializer,
)
from server.apps.g_mtg.models import ProjectSaleChannel
from server.apps.g_mtg.services.project import (
    create_project,
    create_project_sale_channel,
)
from server.apps.services.views import (
    RetrieveListUpdateViewSet,
)
from server.apps.user_request.services.user_reques import (
    create_user_request_with_data_from_file,
    validate_client_data_decoding,
)


class ProjectSaleChannelFilter(django_filters.FilterSet):
    """Фильтр для клиента."""

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'project',
            'sale_channel',
        )


class ProjectSaleChannelViewSet(RetrieveListUpdateViewSet):
    """Продукт банка."""

    serializer_class = ProjectSaleChannelSerializer
    update_serializer_class = UpdateProjectSaleChannelSerializer
    queryset = ProjectSaleChannel.objects.all()
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProjectSaleChannelFilter
    permission_type_map = {
        **RetrieveListUpdateViewSet.permission_type_map,
        'add_client_from_file': 'add_client',
        'add_client_from_postgres': 'add_client',
        'add_client_from_mongo': 'add_client',
        'multiple_create': 'add_channel',
        'statistics': 'statistics',
    }

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client-from-file',
        detail=True,
        serializer_class=UploadDataFromFileSerializer,
    )
    def add_client_from_file(self, request: Request, pk: int):
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

        create_user_request_with_data_from_file(
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

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client-from-postgres',
        detail=True,
        serializer_class=UploadDataFromPostgresSerializer,
    )
    def add_client_from_postgres(self, request: Request, pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        conn = psycopg2.connect(
            dbname=vd['db_name'],
            user=vd['user'],
            password=vd['password'],
            host=vd['host'],
            port=vd['port'],
        )
        cur = conn.cursor()
        cur.execute(vd['db_request'])
        cur.fetchall()

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client-from-mongo',
        detail=True,
        serializer_class=UploadDataFromMongoSerializer,
    )
    def add_client_from_mongo(self, request: Request, pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        client = MongoClient(
            host=vd['host'],
            port=vd['port'],
        )
        db = client[vd['dbname']]
        collection = db[vd['collection_name']]
        result = [data for data in collection.find(vd['db_request'])]


    @action(
        methods=['POST'],
        url_path='multiple-create',
        detail=False,
        serializer_class=MultipleCreateProjectSaleChannelSerializer,
    )
    def multiple_create(self, request: Request):
        """Добавление в проект каналов связи."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_project_sale_channel(
            validated_data=serializer.validated_data,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )
