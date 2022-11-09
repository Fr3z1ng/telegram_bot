from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

b1 = KeyboardButton("/Место_доставки")
b2 = KeyboardButton("/Время_доставки")
b3 = KeyboardButton("/Меню")
b4 = KeyboardButton("/Заказать")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu = InlineKeyboardMarkup()
kb_client.add(b1).add(b2).add(b3)
kb_menu.add(InlineKeyboardButton(f"Заказать", callback_data= f"Заказать"))
