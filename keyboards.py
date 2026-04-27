from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
