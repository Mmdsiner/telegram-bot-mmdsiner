from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import SessionLocal
from services import set_setting
from keyboards import admin_menu
from states import AdminState

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
    await state.set_state(AdminState.discount)
    await message.answer("درصد تخفیف:")

@router.message(AdminState.discount)
async def save_discount(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        await set_setting(session, "discount", message.text)

    await state.clear()
    await message.answer("ثبت شد")
