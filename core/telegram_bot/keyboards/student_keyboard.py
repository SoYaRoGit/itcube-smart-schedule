from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Личные данные',
                callback_data='student_send_personal_data'
            )
        ],
        [
            InlineKeyboardButton(
                text='Расписание',
                callback_data='student_send_schedule'
            )
        ],
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='student_panel_cancel'
            )
        ]
    ]
)


inline_keyboard_backward = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='student_inline_keyboard_backward'
            )
        ]
    ]
)