import django_filters

from server.apps.g_mtg.api.serializers.project_user import (
    CreateProjectUserSerializer,
    ProjectUserSerializer,
)
from server.apps.g_mtg.models import ProjectUser
from server.apps.g_mtg.services.crud.project_user import create_project_user
from server.apps.services.filters_mixins import CreatedUpdatedDateFilterMixin
from server.apps.services.views import RetrieveListCreateDeleteViewSet


class ProjectUserFilter(
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр для проектов."""

    class Meta(object):
        model = ProjectUser
        fields = (
            'id',
            'project',
            'user',
            'role',
        )


class ProjectUserViewSet(RetrieveListCreateDeleteViewSet):
    """Пользователь проекта."""

    serializer_class = ProjectUserSerializer
    create_serializer_class = CreateProjectUserSerializer
    queryset = ProjectUser.objects.select_related(
        'project',
        'user',
    )
    ordering_fields = '__all__'
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
    )
    filterset_class = ProjectUserFilter

    def get_queryset(self):  # noqa: WPS615
        """Фильтруем выдачу пользователей."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(project__in=user.projects.all())

    def perform_create(self, serializer):
        """Закрепление пользователя за проектом."""
        serializer.instance = create_project_user(
            validated_data=serializer.validated_data,
        )
