from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject, Command


authrouter = Router()


# Обработчик заглушка для проверки работы бота
@authrouter.message(CommandStart)
async def cmd_start(message: Message):
    await message.reply(
        text=message.text
    )