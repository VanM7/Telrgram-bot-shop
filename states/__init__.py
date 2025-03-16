from aiogram.dispatcher.filters.state import StatesGroup, State
from  .product_state import ProductState
from .checkout_state import CheckoutState
from .sos_state import SosState
from .questions import AnswerState
class CategoryState(StatesGroup):
    title = State()