from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_authentication = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Авторизация',
                callback_data='authentication'
            )
        ]
    ]
)

inline_keyboard_authentication_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='authentication_backward'
            ),
            InlineKeyboardButton(
                text='Продолжить',
                callback_data='authentication_state_login'
            )
        ]
    ]
)


inline_keyboard_authentication_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text = 'Отмена',
                callback_data = 'authentication_state_cancel'
            )
        ]
    ]
)