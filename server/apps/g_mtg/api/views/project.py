import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.g_mtg.api.serializers import (
    CreateProjectSerializer,
    ListProjectSerializer,
    ProjectSerializer,
    UpdateProjectSerializer,
)
from server.apps.g_mtg.models import Project
from server.apps.g_mtg.services.crud.project import create_project
from server.apps.g_mtg.services.statistics import get_statistics
from server.apps.services.filters_mixins import CreatedUpdatedDateFilterMixin
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
        )


class ProjectViewSet(RetrieveListCreateUpdateViewSet):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    serializer_class = ProjectSerializer
    list_serializer_class = ListProjectSerializer
    create_serializer_class = CreateProjectSerializer
    update_serializer_class = UpdateProjectSerializer
    queryset = Project.objects.select_related(
        'product',
    ).prefetch_related(
        'users',
        'sales_channels',
        'projects_sales_channels',
    )
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProjectFilter
    permission_type_map = {
        **RetrieveListCreateUpdateViewSet.permission_type_map,
        'statistics': 'statistics',
    }

    def get_queryset(self):  # noqa: WPS615
        """Фильтруем выдачу проектов."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(users=user)

    def perform_create(self, serializer):
        """Создание проекта и закрепление пользователя за ним."""
        serializer.instance = create_project(
            validated_data=serializer.validated_data,
            user=self.request.user,
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path='statistics',
    )
    def statistics(self, request):  # noqa: WPS210
        """Регистрация пользователя."""
        projects_id = request.query_params.getlist('id')

        return Response(
            data=get_statistics(projects_id=projects_id),
            status=status.HTTP_201_CREATED,
        )
