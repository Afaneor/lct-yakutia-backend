import django_filters
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from server.apps.g_mtg.api.serializers import ProductSerializer, \
    UploadDataSerializer
from server.apps.g_mtg.models import Product


# class ClientFilter(django_filters.FilterSet):
#     """Фильтр для клиента."""
#
#     class Meta(object):
#         model = Product
#         fields = (
#             'id',
#             'external_key',
#             'client_type',
#         )



class ProductViewSet(ModelViewSet):
    """Продукт банка."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering_fields = ['name', 'description']
    search_fields = ['name', 'description']


    # @action(  # type: ignore
    #     methods=['POST'],
    #     url_path='upload-data',
    #     detail=False,
    #     serializer_class=UploadDataSerializer,
    # )
    # def upload_data(self, request: Request):
    #     """Загрузка данных по клиенты."""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     for chunk in request.FILES['file'].chunks():
    #         a = 1
    #         read = csv.reader(chunk, delimiter=',')
    #         for i in read:
    #             a = 1
    #     return Response(
    #         status=status.HTTP_200_OK
    #     )
