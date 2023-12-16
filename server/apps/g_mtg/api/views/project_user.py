import django_filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.g_mtg.api.serializers.project_user import (
    CreateProjectUserSerializer,
    ProjectUserSerializer,
)
from server.apps.g_mtg.models import ProjectUser
from server.apps.g_mtg.services.project_user import (
    create_project_user,
    get_project_user_statistics,
)
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
    permission_type_map = {
        **RetrieveListCreateDeleteViewSet.permission_type_map,
        'statistics': 'statistics',
    }

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

    @action(
        methods=['GET'],
        url_path='statistics',
        detail=False,
    )
    def statistics(self, request):
        """Статистика по пользователям в проекте."""
        statistics_data = get_project_user_statistics(
            queryset=self.filter_queryset(self.get_queryset()),
        )

        return Response(
            data=statistics_data,
            status=status.HTTP_201_CREATED,
        )

