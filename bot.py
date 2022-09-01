import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters.state import State, StatesGroup
from googletrans import Translator
import keyboards as kb
from config import TOKEN

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


class OS(StatesGroup):
    english_word = State()
    russian_word = State()
    invalid_word = State()


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    name = msg.from_user.first_name
    await msg.answer(
        f"Привет {name}!\nДавай познакомимся меня зовут,Leo!\nДавай вместе начнем изучение слов на английском языке")
    await bot.send_message(msg.chat.id, all_commands)


@dp.callback_query_handler(state=OS.russian_word, run_task='translationtoenglish')
@dp.message_handler(commands=['translationfromenglish'])
async def translation_from_English(msg: types.Message):
    await msg.answer("Напиши слово на английском")
    await OS.english_word.set()


@dp.message_handler(state=OS.english_word)
async def waiting_message_state(msg: types.Message, state: FSMContext):
    word = msg.text
    await state.update_data(english_word=word)
    translator = Translator()
    result = translator.translate(word, 'ru')
    await bot.send_message(msg.chat.id, result.text)
    print("LOG TRANSLATE INFO: " + result.text)
    await state.finish()


@dp.message_handler(commands=['translationtoenglish'])
async def translation_to_English(msg: types.Message):
    await msg.answer("Напиши слово, которое ты хочешь перевести на английский")
    await OS.russian_word.set()


@dp.message_handler(state=OS.russian_word)
async def waiting_message_state(msg: types.Message, state: FSMContext):
    word = msg.text
    await state.update_data(russian_word=word)
    translator = Translator()
    result = translator.translate(word, 'en')
    await bot.send_message(msg.chat.id, result.text)
    print("LOG TRANSLATE INFO: " + result.text)
    await bot.send_message(msg.chat.id, "Хочешь сохранить это слово в словарь ?", reply_markup=kb.markup_buttons_save)
    await state.finish()


@dp.message_handler(commands=['test'])
async def test(msg: types.Message):
    await bot.send_message(msg.chat.id, "test message")

@dp.message_handler(commands=['test'])
async def test(msg: types.Message):
    await bot.send_message(msg.chat.id, "test message")


# @dp.message_handler(content_types=['text'])
# async def text_var(msg: types.Message):
#     word = msg.text
#     translator = Translator()
#     result = translator.translate(word, 'ru')
#     await bot.send_message(msg.chat.id, result.text)
#     print("LOG TRANSLATE INFO: " + result.text)


all_commands = text(
    "Вот список того, что я умею:"
    "\n/start - начало работы"
    "\n/translationfromenglish - ввести слово на английском, которое ты хочешь перевести"
    "\n/translationtoenglish - перевести слово на английский "
    "\n/test - send test message"
)
executor.start_polling(dp, skip_updates=True)
