#from smtpd import usage

from aiogram import  types
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from aiogram import executor
from logging import basicConfig, INFO

from data.config import ADMINS
from loader import dp, db, bot

from filters import IsAdmin, IsUser
from handlers.user.menu import admin_menu, user_menu
from handlers.user.sos import cmd_sos  # Импорт функции из sos.py
from states import SosState

import handlers

user_message = 'Пользователь'
admin_message = 'Админ'
menu_message = 'Меню'
sos_message = 'SOS'

def user_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(menu_message, sos_message)
    return markup

def admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(menu_message,)
    return markup


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(user_message, admin_message)
    await  message.answer('''Привет! 👋

🤖 Я бот-магазин по подаже товаров любой категории.

🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся 
товары возпользуйтесь командой /menu.

❓ Возникли вопросы? Не проблема! Команда /sos поможет 
связаться с админами, которые постараются как можно быстрее откликнуться.
    ''', reply_markup=markup)

@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in ADMINS:
        ADMINS.append(cid)
    await  message.answer('Включен админский режим.',
                          reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите действие:', reply_markup=admin_keyboard())

@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in ADMINS:
        ADMINS.remove(cid)

    await message.answer('Включен пользователбский режим',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите действие:', reply_markup=user_keyboard())

@dp.message_handler(IsAdmin(), text=menu_message)
async def admin_menu_button(message: Message):
    await admin_menu(message)

@dp.message_handler(IsUser(), text=menu_message)
async def user_menu_button(message: Message):
    await user_menu(message)

@dp.message_handler(text=sos_message)
async def process_sos_button(message: Message):
    await cmd_sos(message)

async def on_startup(dp):
    basicConfig(level=INFO)
    db.crate_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)