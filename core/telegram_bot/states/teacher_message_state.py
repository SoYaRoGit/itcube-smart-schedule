from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.methods import EditMessageText
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from telegram_bot.loader import bot



teacher_message_state_router = Router()