from django.utils.translation import gettext_lazy as _
from rest_framework.routers import APIRootView

from server.apps.g_mtg.api.views import (  # ProjectSaleChannelViewSet,; ProjectUserViewSet,
    ProductViewSet,
    ProjectSaleChannelViewSet,
    ProjectUserViewSet,
    ProjectViewSet,
    SaleChannelViewSet,
)
from server.apps.services.custom_router.api_router import ApiRouter
from server.apps.services.custom_router.nested_router import (
    NestedDefaultRouter,
)


class GMtgAPIRootView(APIRootView):
    """Корневой view для app."""

    __doc__ = _('Приложение G-MTG')
    name = _('g_mtg')


router = ApiRouter()
router.APIRootView = GMtgAPIRootView

router.register('projects', ProjectViewSet, 'projects')
router.register('products', ProductViewSet, 'products')
router.register('sales-channels', SaleChannelViewSet, 'sales-channels')
router.register(
    'projects-sales-channels',
    ProjectSaleChannelViewSet,
    'projects-sales-channels',
)
router.register('projects-users', ProjectUserViewSet, 'projects-users')
