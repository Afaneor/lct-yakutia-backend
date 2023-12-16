import django_filters

from server.apps.g_mtg.api.serializers import ProductSerializer
from server.apps.g_mtg.models import Product
from server.apps.services.views import BaseReadOnlyViewSet


class ProductFilter(django_filters.FilterSet):
    """Фильтр для клиента."""

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
    queryset = Product.objects.all()
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = ProductFilter
