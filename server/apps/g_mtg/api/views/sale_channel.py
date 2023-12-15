import django_filters

from server.apps.g_mtg.api.serializers.sale_channel import SaleChannelSerializer
from server.apps.g_mtg.models import SaleChannel
from server.apps.services.views import BaseReadOnlyViewSet


class SaleChannelFilter(django_filters.FilterSet):
    """Фильтр для клиента."""

    class Meta(object):
        model = SaleChannel
        fields = (
            'id',
            'name',
            'key_name',
            'description',
        )


class SaleChannelViewSet(BaseReadOnlyViewSet):
    """Продукт банка."""

    serializer_class = SaleChannelSerializer
    queryset = SaleChannel.objects.all()
    ordering_fields = '__all__'
    search_fields = (
        'name',
    )
    filterset_class = SaleChannelFilter
