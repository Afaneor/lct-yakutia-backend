import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from server.apps.bot.keyboards.event import get_button_for_available_events
from server.apps.bot.keyboards.general import (
    general_keyboard,
)
from server.apps.bot.keyboards.participant import participant_keyboard
from server.apps.bot.keyboards.workout import get_button_for_available_workouts
from server.apps.bot.services.enum import EntityActionType

router = Router()


@router.message(Command(commands=['start']))
async def start(message: types.Message, state: FSMContext):
    """Приветственное слово."""
    await state.update_data(telegram_user_id=str(message.from_user.id))
    await message.answer(
        text=(
            'Вас приветствует ВТУЦ "Вятичъ"! Узнайте всю необходимую '
            'информацию о ближайших мероприятиях нашего центра.'
        ),
        reply_markup=general_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(Command(commands=['help_me']))
@router.message(F.text.lower() == 'помощь')
async def help_me(message: types.Message):
    """Раздел помощи."""
    await message.answer(
        text='Возникли вопросы или есть предложения?\nПишите @GlebMazur',
        reply_markup=general_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(Command(commands=['contacts']))
@router.message(F.text.lower() == 'контакты')
async def contacts(message: types.Message):
    """Раздел контактов."""
    await message.answer(
        text=(
            'Группа в ВК: https://vk.com/vtyc_vyatichi\n'
            'Группа в Telegram: t.me/vtyc_vyatichi\n'
            'Сайт: https://csp-vyatich.ru/\n'
            'Телефон сотрудничества: +7-910-202-6101\n'
            'Телефон для справки: +7-919-200-3829\n'
            'Адрес: г. Орел, ул. Васильевская, 138\n'
        ),
        reply_markup=general_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(Command(commands=['event']))
@router.message(F.text.lower() == 'информация о мероприятиях и запись на них')
async def event(message: types.Message, state: FSMContext):
    """Раздел информации о мероприятиях."""
    available_events_button = await get_button_for_available_events()
    if available_events_button:
        await state.update_data(
            entity_action=EntityActionType.EVENT.value,
        )
        await message.answer(
            text=f'Выберите интересующее мероприятие:',
            reply_markup=available_events_button,
        )
    else:
        await message.answer(
            text=(
                'На данный момент отсутствует информация по ближайшим '
                'мероприятиям. Чтобы получать информацию первым, подпишитесь '
                'на рассылку.'
            )
        )


@router.message(Command(commands=['workout']))
@router.message(F.text.lower() == 'информация о тренировках и запись на них')
async def workout(message: types.Message, state: FSMContext):
    """Раздел информации о мероприятиях."""
    available_workouts_button = await get_button_for_available_workouts()
    if available_workouts_button:
        await state.update_data(
            entity_action=EntityActionType.WORKOUT.value,
        )
        await message.answer(
            text=f'Выберите интересующую тренировку:',
            reply_markup=available_workouts_button,
        )
    else:
        await message.answer(
            text=(
                'На данный момент отсутствует информация по ближайшим '
                'тренировкам.'
            )
        )


@router.message(Command(commands=['participant']))
@router.message(F.text.lower() == 'мой профиль')
async def participant(message: types.Message, state: FSMContext):
    """Раздел профиля участника."""
    await state.update_data(
        entity_action=EntityActionType.PARTICIPANT.value,
    )
    await message.answer(
        text='Выберите нужное действие:',
        reply_markup=participant_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(Command(commands=['about_us']))
@router.message(F.text.lower() == 'о нас')
async def about_us(message: types.Message):
    """Раздел о нас."""
    await message.answer(
        text=(
            'ВТУЦ "Вятичъ" - осуществляет теоретическую и практическую '
            'подготовку граждан по следующим направлениям:\n'
            '- индивидуальная подготовка бойца;\n'
            '- групповая подготовка;\n'
            '- само и взаимопомощь (тактическая медицина);\n'
            '- работа на БПЛА (Беспилотный летательный аппарат);\n'
            '- базовая инженерная подготовка;\n'
            '- экипировка.\n\n'
            'Данный бот позволяет узнать расписание мероприятий, которые '
            'организует ВТУЦ "Вятичъ" и записаться на них.\n '
            'Бот предоставляет информацию о сроках, месте, стоимости и '
            'необходимом оборудовании для успешного участия в мероприятиях.'
        ),
        reply_markup=general_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(F.text.lower() == 'главное меню')
async def main_menu(message: types.Message, state: FSMContext):
    """Главное меню.

    Затираем данные, чтобы не поломалась логика.
    """
    state_data = await state.get_data()
    state_data.pop('event_name', None)
    state_data.pop('workout_name', None)
    state_data.pop('entity_action', None)
    state_data.pop('profile_action', None)
    await message.answer(
        text=f'Выберите действие:',
        reply_markup=general_keyboard.as_markup(resize_keyboard=True),
    )


@router.message(F.text.lower() == 'QAZwsx1!')
async def admin(message: types.Message, state: FSMContext):
    """Расширенный функционал для админа."""
    available_events_button = await get_button_for_available_events()
    if available_events_button:
        await state.update_data(
            entity_action=EntityActionType.ADMIN.value,
        )
        await message.answer(
            text=f'Выберите интересующее мероприятие:',
            reply_markup=available_events_button,
        )
    else:
        await message.answer(
            text=(
                'На данный момент отсутствует информация по ближайшим '
                'мероприятиям. Чтобы получать информацию первым, подпишитесь '
                'на рассылку.'
            )
        )
