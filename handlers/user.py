from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from database import SessionLocal
from models import User, Order
from keyboards import main_menu, receipt_kb
from services import calc_price
from config import SUPPORT_ID, ADMIN_ID
from states import BuyState

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    ref_id = None
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])

    async with SessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(id=message.from_user.id, invited_by=ref_id)
            session.add(user)
            await session.commit()

    await message.answer("خوش اومدی", reply_markup=main_menu())

@router.message(lambda m: m.text == "خرید سرویس")
async def buy(message: types.Message, state: FSMContext):
    await state.set_state(BuyState.count)
    await message.answer("تعداد گیگ رو وارد کن")

@router.message(BuyState.count)
async def process_count(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return

    count = int(message.text)

    async with SessionLocal() as session:
        total = await calc_price(session, "normal", count)
        order = Order(user_id=message.from_user.id, amount=total, status="pending")
        session.add(order)
        await session.commit()

    await state.clear()
    await message.answer(f"مبلغ: {total}\nرسید رو ارسال کن")

@router.message(lambda m: m.photo)
async def receipt(message: types.Message):
    photo_id = message.photo[-1].file_id

    async with SessionLocal() as session:
        result = await session.execute(
            select(Order).where(
                Order.user_id == message.from_user.id,
                Order.status == "pending"
            )
        )
        order = result.scalar()

        if not order:
            await message.answer("سفارشی پیدا نشد")
            return

        order.receipt = photo_id
        await session.commit()

        await message.answer("رسید ثبت شد")

        await message.bot.send_photo(
            ADMIN_ID,
            photo=photo_id,
            caption=f"سفارش #{order.id}\nکاربر: {message.from_user.id}\nمبلغ: {order.amount}",
            reply_markup=receipt_kb(order.id)
        )

@router.message(lambda m: m.text == "پشتیبانی")
async def support(message: types.Message):
    await message.answer(f"{SUPPORT_ID}")
