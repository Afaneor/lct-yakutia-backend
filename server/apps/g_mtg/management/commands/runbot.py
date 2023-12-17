import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from django.conf import settings
from django.core.management.base import BaseCommand

from server.apps.telegram_bot import general

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
general.register_handlers_other(dp)


class Command(BaseCommand):
    """Команда для запуска телеграм бота."""
    help = 'python manage.py runbot'

    def handle(self, *args, **options):
        """Запуск бота."""

        executor.start_polling(dp, skip_updates=True)
