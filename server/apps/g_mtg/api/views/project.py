import django_filters
from django.utils.translation import gettext_lazy as _

from server.apps.g_mtg.api.serializers import (
    CreateProjectSerializer,
    ListProjectSerializer,
    ProjectSerializer,
    UpdateProjectSerializer,
)
from server.apps.g_mtg.models import Project
from server.apps.g_mtg.services.project import (
    create_project,
)
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
    )
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProjectFilter

    def get_queryset(self):  # noqa: WPS615
        """Фильтруем выдачу проектов."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(users=user)

    def perform_create(self, serializer):
        """Закрепление пользователя за проектом."""
        serializer.instance = create_project(
            validated_data=serializer.validated_data,
            user=self.request.user,
        )
