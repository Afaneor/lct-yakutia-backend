from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для добавления данных."""

    help = 'Добавление данных'

    def handle(self, *args, **kwargs):  # noqa: WPS110, WPS213
        """Логика добавления тегов."""
        pass