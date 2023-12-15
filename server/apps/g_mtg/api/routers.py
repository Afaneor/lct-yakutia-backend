from django.utils.translation import gettext_lazy as _
from drf_nova_router.api_router import ApiRouter
from rest_framework.routers import APIRootView

from server.apps.g_mtg.api.views import (
    ProductViewSet,
    ProjectViewSet,
)


class GGmpAPIRootView(APIRootView):
    """Корневой view для app."""

    __doc__ = _('Приложение GGmp')
    name = _('g_mtg')


router = ApiRouter()

router.APIRootView = GGmpAPIRootView
router.register('projects', ProjectViewSet, 'projects')
router.register('products', ProductViewSet, 'products')
