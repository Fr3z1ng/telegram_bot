from aiogram import types, Dispatcher

from create_bot import dp, bot
from keybords import kb_client
from data_base import sqlite_db


# Описание кнопки Start
# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом")


# @dp.message_handler(commands=["Время_доставки"])
async def seller_bot_command(message: types.Message):
    await bot.send_message(message.from_user.id, "По записи в боте основное время доставки от 18.30 - 21.00")


# @dp.message_handler(commands=["Место_доставки"])
async def seller_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Метро Октрябрьская")


async def bot_menu_command(message: types.Message):
    await sqlite_db.sql_menu(message)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(seller_bot_command, commands=["Время_доставки"])
    dp.register_message_handler(seller_place_command, commands=["Место_доставки"])
    dp.register_message_handler(bot_menu_command, commands=["Меню"])

