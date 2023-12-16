import django_filters
from rest_framework.decorators import action

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
    # permission_type_map = {
    #     **BaseReadOnlyViewSet.permission_type_map,
    #     'statistics': 'statistics',
    # }
    #
    # @action(
    #     methods=['GET'],
    #     url_path='statistics',
    #     detail=True,
    # )
    # def statistics(self, request: Request, pk: int):
    #     """Статистика по проекту."""
    #     statistics_data = get_statistics(
    #         project=self.get_object(),
    #     )
    #
    #     return Response(
    #         data=statistics_data,
    #         status=status.HTTP_200_OK,
    #     )