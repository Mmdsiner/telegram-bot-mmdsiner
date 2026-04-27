from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.photo)
async def receipt(message: Message):
    await message.answer("رسید دریافت شد ✅")
