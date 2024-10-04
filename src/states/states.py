from aiogram.filters.state import State, StatesGroup


class FSMChoosingWorkout(StatesGroup):
    fill_phone = State()
    fill_date = State()
