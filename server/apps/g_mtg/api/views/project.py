import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.g_mtg.api.serializers import (
    CreateProjectSerializer,
    ProjectSerializer,
    UpdateProjectSerializer,
)
from server.apps.g_mtg.api.serializers.project import \
    CreateProjectSaleChannelSerializer
from server.apps.g_mtg.models import Project
from server.apps.g_mtg.services.project import create_project, \
    create_project_sale_channel, get_statistics
from server.apps.services.filters_mixins import (
    CreatedUpdatedDateFilterMixin,
)
from server.apps.services.views import RetrieveListCreateUpdateViewSet


class ProjectFilter(
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр для проектов."""

    product_name = django_filters.AllValuesMultipleFilter(
        field_name='product__name',
        label=_('Множественный поиск по названию продукта'),
    )

    class Meta(object):
        model = Project
        fields = (
            'id',
            'users',
            'sales_channels',
            'product',
            'product_name',
            'name',
            'description',
            'prompt',
        )


class ProjectViewSet(RetrieveListCreateUpdateViewSet):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    serializer_class = ProjectSerializer
    create_serializer_class = CreateProjectSerializer
    update_serializer_class = UpdateProjectSerializer
    queryset = Project.objects.select_related(
        'product',
    ).prefetch_related(
        'users',
        'sales_channels',
    )
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProjectFilter
    permission_type_map = {
        **RetrieveListCreateUpdateViewSet.permission_type_map,
        'upload_data': None,
    }

    def get_queryset(self):  # noqa: WPS615
        """Фильтруем выдачу проектов."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(users=user)

    def perform_create(self, serializer):
        """Закрепление пользователя за проектом."""
        validated_data = serializer.validated_data
        serializer.instance = create_project(
            validated_data=validated_data,
            user=self.request.user,
        )

    @action(
        methods=['POST'],
        url_path='add-sales-channels',
        detail=True,
        serializer_class=CreateProjectSaleChannelSerializer,
    )
    def add_sales_channels(self, request: Request, pk: int):
        """Добавление в проект каналов связи."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_project_sale_channel(
            project=self.get_object(),
            validated_data=serializer.validated_data,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=['GET'],
        url_path='statistics',
        detail=True,
    )
    def statistics(self, request):
        """Статистика по проекту."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        statistics_data = get_statistics(
            project=self.get_object(),
        )

        return Response(
            data=statistics_data,
            status=status.HTTP_201_CREATED,
        )
