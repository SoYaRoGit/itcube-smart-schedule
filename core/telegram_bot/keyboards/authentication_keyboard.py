from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_authentication = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Авторизация',
                callback_data='authentication_user'
            )
        ]
    ]
)