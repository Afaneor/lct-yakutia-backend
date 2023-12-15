import django_filters
from rest_framework.viewsets import ModelViewSet

from server.apps.g_mtg.api.serializers import ProjectSerializer
from server.apps.g_mtg.models import Project
from django.utils.translation import gettext_lazy as _
from server.apps.services.filters_mixins import CreatedUpdatedDateFilterMixin, \
    UserFilterMixin


class ProjectFilter(
    UserFilterMixin,
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
            'user',
            'product',
            'product_name',
            'name',
            'description',
            'prompt',
        )


class ProjectViewSet(ModelViewSet):
    """Проект.

    Сущность для аккумуляции продукта, канала продажи и пользователей.
    """

    serializer_class = ProjectSerializer
    queryset = Project.objects.select_related(
        'user',
        'product',
    )
    ordering_fields = '__all__'
    search_fields = (
        'name',
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'product__name',
    )
    filterset_class = ProjectFilter
