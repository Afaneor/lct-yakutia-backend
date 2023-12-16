from django.utils.translation import gettext_lazy as _
from rest_framework.routers import APIRootView

from server.apps.services.custom_router.api_router import ApiRouter
from server.apps.user_request.api.views import MessageViewSet
from server.apps.user_request.api.views.user_request import UserRequestViewSet


class GMtgAPIRootView(APIRootView):
    """Корневой view для app."""

    __doc__ = _('Приложение запросов пользователя')
    name = _('user_request')


router = ApiRouter()
router.APIRootView = GMtgAPIRootView

router.register('messages', MessageViewSet, 'messages')
router.register('users-requests', UserRequestViewSet, 'users-requests')
