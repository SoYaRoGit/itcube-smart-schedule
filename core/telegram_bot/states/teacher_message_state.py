from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from telegram_bot.loader import bot
from telegram_bot.filters.filter import CallbackTeacherGroupsFilter
from telegram_bot.eduutils.edu_utils_db import get_students_group_telegram_id, get_students_group_full_name
from telegram_bot.loader import bot
from telegram_bot.keyboards.teacher_message_state_keyboard import inline_keyboard_teacher_message_state_menu
from asgiref.sync import sync_to_async



teacher_message_state_router = Router()


class FSMTeacherSendMessageForm(StatesGroup):
    MESSAGE = State()



@teacher_message_state_router.callback_query(CallbackTeacherGroupsFilter())
async def teacher_message_state_start(callback: CallbackQuery, group: str, state: FSMContext):
    student_name = await sync_to_async(get_students_group_full_name)(group)
    await state.update_data(name_group=group, student_names = student_name)
    
    await callback.message.edit_text(
        text = f'Подтвердите выбор выбранной группы: {group}',
        reply_markup = inline_keyboard_teacher_message_state_menu
    )
    # await state.set_state(FSMTeacherSendMessageForm.MESSAGE)
    await callback.answer()
    

@teacher_message_state_router.callback_query(F.data.in_('teacher_message_state_menu_confirm'))
async def teacher_message_state_menu_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    # Получаем информацию о группе и студентах
    group_name = data.get('name_group', '')
    student_names = data.get('student_names', [])
    
    # Создаем строку с именами студентов
    student_names_str = ", ".join(student_names)
    
    # Формируем текст сообщения
    message_text = (
        f'Вы успешно выбрали группу: {group_name}\n\n'
        f'Студенты, которые будут уведомлены:\n{student_names_str}'
    )
    
    # Отправляем сообщение
    await state.set_state(state=FSMTeacherSendMessageForm.MESSAGE)
    await callback.message.answer(message_text)

@teacher_message_state_router.message(StateFilter(FSMTeacherSendMessageForm.MESSAGE))
async def FSMTeacherSendMessageForm_MESSAGE(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_ids = await sync_to_async(get_students_group_telegram_id)(data['name_group'])
    print(telegram_ids)
    for telegram_id in telegram_ids:
        await bot.send_message(
            chat_id = telegram_id,
            text = f'[ОПОВЕЩЕНИЕ]\n{message.text}'
        )
    
    await message.answer(text=f'Вы успешно отправили сообщение группе: {data["name_group"]}')
    await state.clear()