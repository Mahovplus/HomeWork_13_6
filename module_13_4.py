from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7576418794:AAEtKzpYh-fVFGWTtopWkc92gD50pnxkZzE"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    """ Инициализация класса """
    age = State()
    growth = State()
    wight = State()


start_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать')],
    [KeyboardButton(text='Информация')]],
    resize_keyboard=True)

# Создание инлайн клавиатуры
kb_il = InlineKeyboardMarkup()
button_in1 = InlineKeyboardButton(text='Рассчитать норму кармы', callback_data='calories')  # >>> set_age
button_in2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formules')  # >>> get_formulas
kb_il.add(button_in1, button_in2)


@dp.message_handler(commands=['start'])
async def answ_button(message):
    await message.answer('Привет, я бот помогающий твоей духовной просвещенности', reply_markup=start_menu)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb_il)


@dp.callback_query_handler(text='formules')
async def get_formulas(call):
    await call.message.answer(' Упрощенный вариант формулы Миффлина-Сан Жеора:\
                            \nдля мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;\
                            \nдля женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.')
    await call.answer()

@dp.callback_query_handler(text='calories')  # Функция - реакция на определенные сообщения
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()  # Запуск видоизменяющейся цепочки состояний от полученной, новой информации


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост.")
    await UserState.growth.set()  # 1-ое звено


@dp.message_handler(state=UserState.growth)
async def set_wight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес.")
    await UserState.wight.set()  # 2-ое звено


@dp.message_handler(state=UserState.wight)
async def send_calories(message, state):
    await state.update_data(wight=message.text)
    data = await  state.get_data()  # Хранилище полученных данных в виде словаря (значение в строковом представление)
    await message.answer(f"Ваша норма кармической деятельности на каждый день: "
                         f" {10 * int(data['wight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}\n"
                         "Процентное соотношение из скверных мыслей и действий.\n"
                         "Максимально допустимое значение в день - 0.00000000000001.\n"
                         "Пожалуйста, задумайтесь. Прощайте, Человек.")
    # Реализация формулы подсчета калорий из полученных данных
    await state.finish()  # Завершающее звено цепочки


@dp.message_handler()
async def all_message(message):
    await message.answer("Привет! Я бот способствующий твоему духовному развитию. \
                         Я могу высчитать норму твоей кармической деятельности на каждый день.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
