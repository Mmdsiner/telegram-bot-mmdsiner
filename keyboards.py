from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="خرید سرویس")],
            [KeyboardButton(text="پشتیبانی")]
        ],
        resize_keyboard=True
    )

def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="تنظیم قیمت معمولی")],
            [KeyboardButton(text="تنظیم قیمت ویژه")],
            [KeyboardButton(text="تنظیم کارت")],
            [KeyboardButton(text="تنظیم تخفیف")]
        ],
        resize_keyboard=True
    )

def receipt_kb(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ تایید", callback_data=f"ok_{order_id}"),
                InlineKeyboardButton(text="❌ رد", callback_data=f"no_{order_id}")
            ]
        ]
    )
