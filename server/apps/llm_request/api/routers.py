from django.utils.translation import gettext_lazy as _
from rest_framework.routers import APIRootView

from server.apps.llm_request.api.views import (
    MessageViewSet,
    RequestDataViewSet,
)
from server.apps.services.custom_router.api_router import ApiRouter


class GMtgAPIRootView(APIRootView):
    """Корневой view для app."""

    __doc__ = _('Приложение запросов пользователя')
    name = _('request_data')


router = ApiRouter()
router.APIRootView = GMtgAPIRootView

router.register('messages', MessageViewSet, 'messages')
router.register(
    'requests-data',
    RequestDataViewSet,
    'requests-data',
)
