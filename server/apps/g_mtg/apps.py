from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GGmpConfig(AppConfig):
    """Конфиг приложения генерации предложений."""

    name = 'server.apps.g_mtg'
    verbose_name = _('Генерация предложений')

    def ready(self) -> None:
        """Подключение прав происходит при подключении app."""
        import server.apps.g_mtg.api.routers
        import server.apps.g_mtg.permissions
