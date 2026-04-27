from aiogram.fsm.state import StatesGroup, State

class BuyState(StatesGroup):
    amount = State()
