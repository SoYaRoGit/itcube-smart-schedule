from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура с кнопкой авторизации
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

# Клавиатура с окном подтверждения
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

# Клавиатура с отменой(удаление)
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

# Клавиатура для подтверждения введенных данных
inline_keyboard_authentication_check = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='authentication_state_cancel'
            ),
            InlineKeyboardButton(
                text='Ввести заново',
                callback_data='authentication_state_login'
            )

        ],
        [
            InlineKeyboardButton(
                text='Авторизация',
                callback_data='authentication_check'
            )
        ]
    ]
)