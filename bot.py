from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'
    work_experience = State()  # Состояние для опыта работы
    confirm = State()  # Состояние для подтверждения правильности введенных данных

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await Form.name.set()  # Set state
    await message.reply(main_text)

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply(text_age)

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await Form.next()
    await message.reply(text_gender)

@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await Form.next()
    await message.reply(text_work)

@dp.message_handler(state=Form.work_experience)
async def process_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['work_experience'] = message.text

    # Выводим пользователю данные и спрашиваем подтверждение
    user_data = (
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Пол: {data['gender']}\n"
        f"Опыт работы: {data['work_experience']}"
    )
    await message.reply(user_data)
    await message.reply("Всё ли введено верно? (да/нет)")
    await Form.confirm.set()  # Переход к состоянию подтверждения

@dp.message_handler(state=Form.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.reply(text_end_2)
        await state.finish()  # Завершаем машину состояний
    elif message.text.lower() == 'нет':
        await message.reply("Давайте начнем заново.")
        await Form.name.set()  # Возвращаемся к началу формы
    else:
        await message.reply("Пожалуйста, ответьте 'да' или 'нет'.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
