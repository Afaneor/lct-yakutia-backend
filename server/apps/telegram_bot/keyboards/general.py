"""https://mastergroosha.github.io/aiogram-3-guide/buttons/"""
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

general_keyboard = ReplyKeyboardBuilder()


general_keyboard.row(
    KeyboardButton(text='Информация о мероприятиях и запись на них'),
)
general_keyboard.row(
    KeyboardButton(text='Информация о тренировках и запись на них'),
)
general_keyboard.row(
    KeyboardButton(text='Мой профиль'),
)
general_keyboard.row(
    KeyboardButton(text='О нас'),
    KeyboardButton(text='Контакты'),
    KeyboardButton(text='Помощь'),
)


cancellation_action = ReplyKeyboardBuilder()

cancellation_action.row(
    KeyboardButton(text='Отмена'),
)
