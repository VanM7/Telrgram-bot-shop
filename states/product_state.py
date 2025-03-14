from aiogram.dispatcher.filters.state import StatesGroup, State

class Category(StatesGroup):
    title = State()

class ProductState(StatesGroup):
    title = State()
    body = State()
    image = State()
    price = State()
    confirm = State()
