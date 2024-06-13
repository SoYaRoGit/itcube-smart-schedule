from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура меню преподавателя для подтверждения выбранной группы
inline_keyboard_teacher_message_state_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='teacher_inline_keyboard_backward'
            )
        ],
        [
            InlineKeyboardButton(
                text = 'Подтвердить',
                callback_data = 'teacher_message_state_menu_confirm'
            )
        ]
    ]
)