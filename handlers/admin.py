from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from config import ADMIN_ID
from database import SessionLocal
from services import set_setting, add_success_invite
from keyboards import admin_menu
from states import AdminState
from models import Order, User

router = Router()

def is_admin(user_id):
    return user_id == ADMIN_ID

@router.message(lambda m: m.from_user.id == ADMIN_ID)
async def admin_panel(message: types.Message):
    await message.answer("پنل ادمین", reply_markup=admin_menu())

@router.message(lambda m: m.text == "تنظیم قیمت معمولی")
async def set_normal(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminState.price)
    await message.answer("قیمت جدید:")

@router.message(AdminState.price)
async def save_price(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    if not message.text.isdigit():
        return

    async with SessionLocal() as session:
        await set_setting(session, "normal_price", message.text)

    await state.clear()
    await message.answer("ثبت شد")

@router.message(lambda m: m.text == "تنظیم کارت")
async def set_card(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminState.card)
    await message.answer("شماره کارت:")

@router.message(AdminState.card)
async def save_card(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        await set_setting(session, "card", message.text)

    await state.clear()
    await message.answer("ثبت شد")

@router.message(lambda m: m.text == "تنظیم تخفیف")
async def set_discount(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminState.discount)
    await message.answer("درصد تخفیف:")

@router.message(AdminState.discount)
async def save_discount(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        await set_setting(session, "discount", message.text)

    await state.clear()
    await message.answer("ثبت شد")

@router.callback_query(lambda c: c.data.startswith("ok_"))
async def confirm_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    async with SessionLocal() as session:
        order = await session.get(Order, order_id)
        if not order:
            return

        order.status = "paid"

        user = await session.get(User, order.user_id)

        if user and user.invited_by:
            await add_success_invite(session, user.invited_by)

        await session.commit()

        await callback.message.edit_caption(callback.message.caption + "\n✅ تایید شد")

        await callback.bot.send_message(
            order.user_id,
            "✅ پرداخت تایید شد\nسرویس شما:\nusername: test\npassword: test"
        )

    await callback.answer("تایید شد")

@router.callback_query(lambda c: c.data.startswith("no_"))
async def reject_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    async with SessionLocal() as session:
        order = await session.get(Order, order_id)
        if not order:
            return

        order.status = "rejected"
        await session.commit()

        await callback.message.edit_caption(callback.message.caption + "\n❌ رد شد")

        await callback.bot.send_message(
            order.user_id,
            "❌ پرداخت رد شد"
        )

    await callback.answer("رد شد")
