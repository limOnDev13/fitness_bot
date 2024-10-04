from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.exercises import exercises


def get_keyboard_with_exercises() -> InlineKeyboardMarkup:
    """The function returns the keyboard to select a workout"""
    buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"{exercise} - {price} руб.", callback_data=exercise)
        for exercise, price in exercises.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
