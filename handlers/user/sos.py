from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default.markups import all_right_message, cancel_message,submit_markup
from aiogram.types import Message
from states import SosState
from loader import dp, db
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Локальная функция для создания простой клавиатуры с кнопкой Меню
def get_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню')  # Добавляем кнопку Меню
    logger.info("Клавиатура создана: %s", markup.keyboard)  # Отладочный вывод
    return markup

@dp.message_handler(commands='sos')
async def cmd_sos(message: Message):
    await SosState.question.set()
    await message.answer('В чем суть проблемы? Опишите как можно детальнее'
        ' и администратор обязательно вам ответит.',
        reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Убедитесь, что все верно.', reply_markup=submit_markup())
    await SosState.next()

@dp.message_handler(
    lambda message: message.text not in [cancel_message, all_right_message],
    state=SosState.submit)
async def process_price_invalid(message: Message):
    await message.answer('Такого варианта не было.')

@dp.message_handler(text=cancel_message, state=SosState.submit)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Oтмененo!',reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text=all_right_message, state=SosState.submit)
async def process_submit(message: Message, state: FSMContext):
    cid = message.chat.id
    markup = get_menu_keyboard()

    try:
        result = db.fetchone('SELECT * FROM questions WHERE cid=?', (cid,))
        logger.info("Результат fetchone: %s", result)
        if result is None:
            async with state.proxy() as data:
                db.query('INSERT INTO questions VALUES (?,?)', (cid, data['question']))
            await message.answer('Отправлено!', reply_markup=markup)
        else:
            await message.answer(
                'Превышен лимит на количество задаваемых вопросов.',
                reply_markup=markup
            )
    except Exception as e:
        logger.error("Ошибка при работе с базой данных: %s", e)
        await message.answer('Произошла ошибка. Попробуйте позже.', reply_markup=markup)

    await state.finish()
