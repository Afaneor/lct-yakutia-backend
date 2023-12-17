import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from django.conf import settings
from django.core.management.base import BaseCommand

from server.apps.bot.handlers import (
    event,
    general,
    participant,
    participant_profile,
    participants_event, admin_event, participants_workout
)


async def on_startup():
    """Запуск бота."""
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(admin_event.router)
    dp.include_router(general.router)
    dp.include_router(event.router)
    dp.include_router(participant.router)
    dp.include_router(participant_profile.router)
    dp.include_router(participants_event.router)
    dp.include_router(participants_workout.router)
    await dp.start_polling(bot)


class Command(BaseCommand):
    """Команда для запуска телеграм бота."""
    help = 'python manage.py runbot'

    def handle(self, *args, **options):
        """Запуск бота."""
        asyncio.run(on_startup(), debug=True)

