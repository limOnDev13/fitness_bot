import logging
from typing import Dict, Any

from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.lexicon.lexicon_ru import LEXICON_RU
from src.keyboards.exercises_keyboard import get_keyboard_with_exercises
from src.database.users import user_data
from src.states.states import FSMChoosingWorkout
from src.filters.filters import PhoneFilter, DateFilter
from src.config.config import load_config


logger = logging.getLogger("main.users")

router: Router = Router()

ADMIN_ID: int = load_config().bot.admin_id


@router.message(CommandStart(), StateFilter(default_state))
async def start_command_process(message: Message):
    """Processing command /start"""
    logger.info("/start from user with id %d", message.from_user.id)
    # Greeting
    await message.answer(
        text=LEXICON_RU["start"],
    )
    # Ask to choose a workout
    await message.answer(
        text=LEXICON_RU["choose_workout"],
        reply_markup=get_keyboard_with_exercises(),
    )


@router.callback_query(StateFilter(default_state))
async def process_chosen_workout(callback: CallbackQuery,
                                 state: FSMContext):
    """Handler handles the selection of a workout"""
    logger.info("Process of choosing exercise")
    exercise: str = callback.data
    logger.debug("User chose %s", exercise)

    # save exercise
    user_data[callback.from_user.id] = {"exercise": exercise}

    # ask to enter phone number
    await callback.message.answer(
        text=LEXICON_RU["chosen_workout"].format(exercise=exercise)
    )
    await state.set_state(FSMChoosingWorkout.fill_phone)


@router.message(StateFilter(FSMChoosingWorkout.fill_phone), PhoneFilter())
async def process_input_phone(message: Message, state: FSMContext):
    """Handler saves phone number"""
    logger.info("Process of input phone number")
    user_data[message.from_user.id]["phone_number"] = message.text
    logger.debug("User's phone number %s", message.text)

    # Ask to choose date
    await message.answer(text=LEXICON_RU["choose_date"])
    await state.set_state(FSMChoosingWorkout.fill_date)


@router.message(StateFilter(FSMChoosingWorkout.fill_phone))
async def process_input_invalid_phone(message: Message):
    """Handler reports that an incorrect number has been entered"""
    logger.warning("User entered an invalid phone number: %s", message.text)
    await message.answer(text=LEXICON_RU["invalid_phone"])


@router.message(StateFilter(FSMChoosingWorkout.fill_date), DateFilter())
async def process_input_date(message: Message, state: FSMContext, bot: Bot):
    """Handler saves date of workout"""
    logger.info("Process of input date and time")
    # save datetime
    user_data[message.from_user.id]["date_time"] = message.text
    logger.debug("User chose date and time: %s", message.text)

    # get all inputs
    exercise = user_data[message.from_user.id]["exercise"]
    phone_number = user_data[message.from_user.id]["phone_number"]

    # reply to user
    await message.answer(text=LEXICON_RU["success_msg_to_user"].format(
        exercise=exercise,
        date_time=message.text,
        phone_number=phone_number
    ))
    # reply to admin
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=LEXICON_RU["success_msg_to_admin"].format(
            phone_number=phone_number, exercise=exercise, date_time=message.text
        )
    )
    # clear state
    await state.clear()


@router.message(StateFilter(FSMChoosingWorkout.fill_date))
async def process_invalid_date(message: Message):
    """Handler reports that an incorrect date has been entered"""
    logger.warning("User entered invalid date and time: %s", message.text)
    await message.answer(LEXICON_RU["invalid_date_time"])
