from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
from database import SessionLocal

router = Router()

# ================== KEYBOARDS ==================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="خرید سرویس")],
        [KeyboardButton(text="پشتیبانی")]
    ],
    resize_keyboard=True
)

service_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="سرویس معمولی")],
        [KeyboardButton(text="سرویس ویژه")],
        [KeyboardButton(text="🔙 برگشت")]
    ],
    resize_keyboard=True
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 برگشت")]
    ],
    resize_keyboard=True
)

# ================== STATES ==================

class BuyState(StatesGroup):
    choosing_type = State()
    entering_amount = State()
    sending_receipt = State()

# ================== HANDLERS ==================

@router.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer("خوش اومدی 👋", reply_markup=main_menu)


@router.message(F.text == "خرید سرویس")
async def buy_service(msg: Message, state: FSMContext):
    await state.set_state(BuyState.choosing_type)
    await msg.answer("نوع سرویس رو انتخاب کن:", reply_markup=service_type_kb)


@router.message(F.text == "🔙 برگشت")
async def back(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("بازگشت به منو", reply_markup=main_menu)


@router.message(BuyState.choosing_type, F.text.in_(["سرویس معمولی", "سرویس ویژه"]))
async def choose_type(msg: Message, state: FSMContext):
    await state.update_data(service_type=msg.text)
    await state.set_state(BuyState.entering_amount)

    await msg.answer("چند گیگ میخوای؟ عدد بفرست:", reply_markup=back_kb)


@router.message(BuyState.entering_amount, F.text.regexp(r"^\d+$"))
async def calculate_price(msg: Message, state: FSMContext):
    data = await state.get_data()

    amount = int(msg.text)
    service_type = data.get("service_type")

    # قیمت نمونه (بعدا از دیتابیس بخون)
    price_per_gb = 400000 if service_type == "سرویس معمولی" else 600000
    total = amount * price_per_gb

    await state.update_data(amount=amount, total=total)

    text = f"""
🧾 فاکتور خرید

📦 نوع سرویس: {service_type}
📊 مقدار: {amount} گیگ
💰 قیمت هر گیگ: {price_per_gb:,} تومان

━━━━━━━━━━━━━━━
💵 مبلغ کل: {total:,} تومان
━━━━━━━━━━━━━━━

لطفا رسید رو ارسال کن 📩
"""

    await state.set_state(BuyState.sending_receipt)
    await msg.answer(text)


@router.message(BuyState.sending_receipt, F.photo)
async def receive_receipt(msg: Message, state: FSMContext):
    data = await state.get_data()

    caption = f"""
📥 سفارش جدید

👤 USER_ID: {msg.from_user.id}
💰 مبلغ: {data.get("total")}
📦 نوع: {data.get("service_type")}
"""

    from handlers.admin import confirm_kb

    await msg.bot.send_photo(
        ADMIN_ID,
        msg.photo[-1].file_id,
        caption=caption,
        reply_markup=confirm_kb
    )

    await msg.answer("رسید ارسال شد ✅ منتظر تایید ادمین باش")
    await state.clear()


@router.message(F.text == "پشتیبانی")
async def support(msg: Message):
    await msg.answer("پشتیبانی:\n@mmdsiner")
