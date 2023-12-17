from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RequestDataConfig(AppConfig):
    """Конфиг приложения запросов пользователя."""

    name = 'server.apps.llm_request'
    verbose_name = _('Запросы пользователя в llm модель')

    def ready(self) -> None:
        """Подключение прав происходит при подключении app."""
        import server.apps.llm_request.api.routers
        import server.apps.llm_request.permissions
