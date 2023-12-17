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
    UpdateProjectSaleChannelSerializer,
    UploadDataFromFileSerializer,
    UploadDataFromMongoSerializer,
    UploadDataFromPostgresSerializer,
)
from server.apps.g_mtg.models import ProjectSaleChannel
from server.apps.g_mtg.services.crud.project import create_project_sale_channel
from server.apps.llm_request.services.user_reques import (
    create_marketing_text_request_with_data_from_xlsx_file,
    validate_client_data_decoding,
    create_marketing_text_request_with_data_from_postgres,
    create_marketing_text_request_with_data_from_mongo,
)
from server.apps.services.views import RetrieveListUpdateViewSet


class ProjectSaleChannelFilter(django_filters.FilterSet):
    """Фильтр для каналов продаж в проекте."""

    class Meta(object):
        model = ProjectSaleChannel
        fields = (
            'id',
            'project',
            'sale_channel',
        )


class ProjectSaleChannelViewSet(RetrieveListUpdateViewSet):
    """Канал продаж в проекте."""

    serializer_class = ProjectSaleChannelSerializer
    update_serializer_class = UpdateProjectSaleChannelSerializer
    queryset = ProjectSaleChannel.objects.select_related(
        'project',
        'sale_channel',
    )
    ordering_fields = '__all__'
    search_fields = (
        'project__name',
        'sale_channel__name',
    )
    filterset_class = ProjectSaleChannelFilter
    permission_type_map = {
        **RetrieveListUpdateViewSet.permission_type_map,
        'add_client_from_xlsx_file': 'add_client',
        'add_client_from_postgres': 'add_client',
        'add_client_from_mongo': 'add_client',
        'multiple_create': 'add_channel',
    }

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client-from-xlsx-file',
        detail=True,
        serializer_class=UploadDataFromFileSerializer,
    )
    def add_client_from_xlsx_file(self, request: Request, pk: int):
        """Загрузка данных из xlsx файла.

        ВНИМАНИЕ.
        Файл, который был прикреплен к заданию не прогрузится.
        Необходимо в последнем элементе файла (на 1001 строке в последнем
        столбце) поставить курсор и нажать delete. Новый файл будет весить на
        10 Кб меньше и прогрузится.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with request.FILES['file'].open(mode='r') as file:
            db = xl.readxl(file)
            all_client_data: List[Dict[str, Any]] = []
            client_data_keys: List[Any] = []
            for list_name in db.ws_names:
                for index, row in enumerate(db.ws(ws=list_name).rows):
                    if index != 0:
                        all_client_data.append(dict(zip(client_data_keys, row)))
                    else:
                        client_data_keys = row

        client_data_decoding = serializer.validated_data['client_data_decoding']
        validate_client_data_decoding(
            client_data_decoding=client_data_decoding,
            client_data_keys=client_data_keys,
        )

        create_marketing_text_request_with_data_from_xlsx_file(
            project_sale_channel=self.get_object(),
            user=self.request.user,
            source_client_info=request.FILES['file'].name,
            all_client_data=all_client_data,
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
        validated_data = serializer.validated_data
        connection = psycopg2.connect(
            dbname=validated_data['db_name'],
            user=validated_data['db_user'],
            password=validated_data['db_password'],
            host=validated_data['db_host'],
            port=validated_data['db_port'],
        )
        pg_cursor = connection.cursor()
        pg_cursor.execute(validated_data['db_request'])

        create_marketing_text_request_with_data_from_postgres(
            project_sale_channel=self.get_object(),
            user=self.request.user,
            source_client_info=f"POSTGRES. DB_NAME: {validated_data['db_name']}",
            all_client_data=pg_cursor.fetchall(),
            client_data_decoding=validated_data['client_data_decoding'],
        )

        return Response(
            data={'detail': _('Данные загружены')},
            status=status.HTTP_201_CREATED
        )

    @action(  # type: ignore
        methods=['POST'],
        url_path='add-client-from-mongo',
        detail=True,
        serializer_class=UploadDataFromMongoSerializer,
    )
    def add_client_from_mongo(self, request: Request, pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        client = MongoClient(
            host=validated_data['db_host'],
            port=validated_data['db_port'],
        )
        db = client[validated_data['db_name']]
        collection = db[validated_data['db_collection_name']]
        all_client_data = [
            data
            for data in collection.find(validated_data['db_request'])
        ]
        client_data_decoding = validated_data['client_data_decoding']

        validate_client_data_decoding(
            client_data_decoding=validated_data['client_data_decoding'],
            client_data_keys=list(all_client_data.keys()),
        )

        create_marketing_text_request_with_data_from_mongo(
            project_sale_channel=self.get_object(),
            user=self.request.user,
            source_client_info=f"MONGO. DB_NAME: {validated_data['db_name']}",
            all_client_data=all_client_data,
            client_data_decoding=client_data_decoding,
        )

        return Response(
            data={'detail': _('Данные загружены')},
            status=status.HTTP_201_CREATED
        )

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
