from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import BuyState

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("🤖 ربات فعال شد")
    await message.answer("چند گیگ میخوای؟")

    await state.set_state(BuyState.amount)

@router.message(BuyState.amount)
async def get_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("عدد بفرست")

    amount = int(message.text)

    await state.update_data(amount=amount)

    await message.answer(f"مقدار ثبت شد: {amount}")
