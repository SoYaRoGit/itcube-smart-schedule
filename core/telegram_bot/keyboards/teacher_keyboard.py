from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.eduutils.edu_utils_db import get_groups_teacher
from asgiref.sync import sync_to_async


# Клавиатура - меню преподавателя
inline_keyboard_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Учетная запись',
                callback_data='teacher_send_personal_data'
            )
        ],
        [
            InlineKeyboardButton(
                text='Расписание',
                callback_data='teacher_send_schedule'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отправить сообщение для группы',
                callback_data='teacher_send_message_for_group'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='teacher_panel_cancel'
            )
        ]
    ]
)

# Клавиатура, которая позвращает в меню
inline_keyboard_backward = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='teacher_inline_keyboard_backward'
            )
        ]
    ]
)


# Клавиатура - строитель, которая выводит список групп
async def builder_inline_keyboard_group(telegram_id_teacher: int) -> InlineKeyboardBuilder:
    inline_keyboard_groups = InlineKeyboardBuilder()
    button_group: list[tuple[str, str]] = await sync_to_async(get_groups_teacher)(telegram_id_teacher)
    
    for button_text, callback_data in button_group:
        inline_keyboard_groups.add(InlineKeyboardButton(
            text = button_text,
            callback_data = callback_data
        ))
    inline_keyboard_groups.add(
        InlineKeyboardButton(
            text = 'Назад',
            callback_data = 'teacher_inline_keyboard_backward'
        )
    )  
    
    inline_keyboard_groups.adjust(1)
    return inline_keyboard_groups.as_markup()