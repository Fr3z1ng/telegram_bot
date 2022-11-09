from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keybords import kb_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = 590180927


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    cost = State()


# проверяю соответствует ли ID админу
async def make_admin(message: types.Message):
    global ID
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, "Привет хозяин", reply_markup=kb_admin.button_case_admin)


# начало загрузки нового пункта меню
# @dp.message_handler(commands="Загрузить", state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото")


# ловим первый ответ пункта меню
# @dp.message_handler(content_types="photo", state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Введи название одноразки")


# пишем название продукта
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание одноразки")


# пишем описание продукта
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply("Введи цену")


# указываем цену
# @dp.message_handler(state=FSMAdmin.cost)
async def load_cost(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["cost"] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()


# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Ок")


async def del_callback_run(callback: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback.data.replace('del ', ''))
    await callback.message.reply("Ваш продукт был удален")
    await callback.answer()


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        menu = await sqlite_db.sql_menu2()
        for ret in menu:
            await bot.send_photo(message.from_user.id, ret[0],
                                 f"Название: {ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"Удалить {ret[1]}", callback_data=f"del {ret[1]}")))


async def no_command(message: types.Message):
    await message.answer("Нет такой команды,введите /start и следуйте инструкции")


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_admin, commands=["admin"])
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_cost, state=FSMAdmin.cost)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands=["Удалить"])
    dp.register_message_handler(no_command)
