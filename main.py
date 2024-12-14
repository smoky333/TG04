import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объекта бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Привет"),
                KeyboardButton(text="Пока")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите опцию:", reply_markup=keyboard)


@dp.message(lambda message: message.text in ["Привет", "Пока"])
async def greet_or_bye(message: types.Message):
    if message.text == "Привет":
        username = message.from_user.first_name
        await message.answer(
            f"Привет, {username}!",
            reply_markup=ReplyKeyboardRemove()
        )
    elif message.text == "Пока":
        username = message.from_user.first_name
        await message.answer(
            f"До свидания, {username}!",
            reply_markup=ReplyKeyboardRemove()
        )


@dp.message(Command('links'))
async def send_links(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новости", url="https://edition.cnn.com/")],
            [InlineKeyboardButton(text="Музыка", url="https://music.youtube.com/")],
            [InlineKeyboardButton(text="Видео", url="https://youtube.com")]
        ]
    )
    await message.answer("Полезные ссылки:", reply_markup=keyboard)


@dp.message(Command('dynamic'))
async def dynamic_keyboard(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )
    await message.answer("Выберите опцию:", reply_markup=keyboard)


@dp.callback_query()
async def handle_callbacks(call: types.CallbackQuery):
    if call.data == "show_more":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
                [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
            ]
        )
        await call.message.edit_text("Выберите опцию:", reply_markup=keyboard)

    elif call.data == "option_1":
        await call.message.answer("Вы выбрали: Опция 1")
        await call.answer()

    elif call.data == "option_2":
        await call.message.answer("Вы выбрали: Опция 2")
        await call.answer()

# Команда /help
@dp.message(Command('help'))
async def help_command(message: types.Message):
    help_text = (
        "Доступные команды:\n\n"
        "/start - Показать главное меню с кнопками 'Привет' и 'Пока'\n"
        "/links - Показать полезные ссылки\n"
        "/dynamic - Показать динамическую клавиатуру\n"
        "/help - Показать список доступных команд\n\n"
        "Описание команд:\n"
        "- При команде /start вы увидите кнопки для приветствия и прощания\n"
        "- /links предоставит вам ссылки на новости, музыку и видео\n"
        "- /dynamic покажет интерактивное меню с возможностью выбора опций"
    )
    await message.answer(help_text)


async def main():
    await dp.start_polling(bot)  # Передаем bot в start_polling


if __name__ == "__main__":
    asyncio.run(main())