from server.apps.g_mtg.api.views.product import ProductViewSet
from server.apps.g_mtg.api.views.project import ProjectViewSet
from server.apps.g_mtg.api.views.project_sale_channel import (
    ProjectSaleChannelViewSet,
)
from server.apps.g_mtg.api.views.project_user import (
    ProjectUserViewSet,
)
from server.apps.g_mtg.api.views.sale_channel import SaleChannelViewSet

__all__ = [
    'ProjectViewSet',
    'ProjectSaleChannelViewSet',
    'ProductViewSet',
    'ProjectUserViewSet',
    'SaleChannelViewSet',
]
