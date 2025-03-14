from aiogram.dispatcher.filters.state import StatesGroup, State
from  .product_state import ProductState

class CategoryState(StatesGroup):
    title = State()