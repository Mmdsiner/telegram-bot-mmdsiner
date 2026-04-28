from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN_ID

router = Router()

confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ تایید", callback_data="ok"),
            InlineKeyboardButton(text="❌ رد", callback_data="reject")
        ]
    ]
)

def extract_user_id(text):
    for line in text.split("\n"):
        if "USER_ID" in line:
            return int(line.split(":")[1].strip())

# ================== CALLBACK ==================

@router.callback_query(F.data == "ok")
async def confirm_order(call: CallbackQuery):
    user_id = extract_user_id(call.message.caption)

    await call.message.answer("حالا سرویس رو بفرست 👇")

    # ذخیره موقت آیدی کاربر
    global WAITING_USER
    WAITING_USER = user_id

    await call.answer("تایید شد")


@router.callback_query(F.data == "reject")
async def reject_order(call: CallbackQuery):
    user_id = extract_user_id(call.message.caption)

    await call.bot.send_message(user_id, "❌ پرداخت شما رد شد")

    await call.answer("رد شد")


# ================== SEND SERVICE ==================

WAITING_USER = None

@router.message(F.chat.id == ADMIN_ID)
async def send_service(msg: Message):
    global WAITING_USER

    if WAITING_USER:
        await msg.bot.send_message(
            WAITING_USER,
            f"✅ سرویس شما:\n\n{msg.text}"
        )

        await msg.answer("ارسال شد ✅")
        WAITING_USER = None
