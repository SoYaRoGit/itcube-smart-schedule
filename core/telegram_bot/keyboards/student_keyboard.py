from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_kyboard_panel = InlineKeyboardMarkup(
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