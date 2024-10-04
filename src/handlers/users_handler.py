import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.lexicon.lexicon_ru import LEXICON_RU
from src.keyboards.exercises_keyboard import get_keyboard_with_exercises


logger = logging.getLogger("main.users")

router: Router = Router()


@router.message(CommandStart())
async def start_command_process(message: Message):
    """Processing command /start"""
    logger.info("/start from user with id %d", message.from_user.id)
    await message.answer(
        text=LEXICON_RU["start"],
        reply_markup=get_keyboard_with_exercises()
    )



