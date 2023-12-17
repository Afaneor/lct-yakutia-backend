import django_filters

from server.apps.g_mtg.api.serializers import (
    ListProductSerializer,
    ProductSerializer,
)
from server.apps.g_mtg.models import Product
from server.apps.services.views import BaseReadOnlyViewSet


class ProductFilter(django_filters.FilterSet):
    """Фильтр для продукта."""

    class Meta(object):
        model = Product
        fields = (
            'id',
            'name',
            'key_name',
            'link',
            'description',
        )


class ProductViewSet(BaseReadOnlyViewSet):
    """Продукт банка."""

    serializer_class = ProductSerializer
    list_serializer_class = ListProductSerializer
    queryset = Product.objects.prefetch_related('projects')
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProductFilter
