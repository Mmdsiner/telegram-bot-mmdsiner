from aiogram.fsm.state import StatesGroup, State

class BuyState(StatesGroup):
    count = State()

class AdminState(StatesGroup):
    price = State()
    card = State()
    discount = State()
