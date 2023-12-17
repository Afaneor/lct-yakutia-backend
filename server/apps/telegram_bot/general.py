from aiogram import Dispatcher, types

from server.apps.llm_request.services.formation_request import (
    get_request_for_get_marketing_text,
)


async def start(message: types.Message):
    """Приветственное слово."""
    await message.answer(
        text=(
            'Вас приветствует бот от Газпромбанка для генерации ' +
            'маркетингового предложения по продуктам банка.' +
            'Напишите информацию, по которой бот сможет сформировать ' +
            'маркетинговое предложение и ожидайте ответа'
        ),
    )


async def help(message: types.Message):
    """Раздел помощи."""
    await message.answer(
        text='Возникли вопросы или есть предложения?\nПишите @GlebMazur',
    )


async def handle_message(message: types.Message):
    # Отправляем сообщение пользователя на стороннюю API
    try:
        response = get_request_for_get_marketing_text(prompt=message.text)
        response.raise_for_status()
        data = response.json()
        # Получаем ответ от API и отправляем его пользователю
        await message.reply(data['response'])
    except Exception as e:
        await message.reply('Произошла ошибка при обработке запроса.')


def register_handlers_other(dp: Dispatcher):
    """Регистрация обработчиков."""
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(handle_message)
