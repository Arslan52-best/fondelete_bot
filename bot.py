if __name__ == "__main__":
    print("Скрипт запущен!")


import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from rembg import remove
from io import BytesIO
from PIL import Image

TOKEN = "7590497355:AAHwp-K_Ibl_whi_Z79IMryQiqFIZsKSra8"

from aiogram.client.default import DefaultBotProperties

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для удаления фона с изображений.\n\n"
        "📌 Как использовать?\n"
        "1️⃣ Отправь мне любое изображение.\n"
        "2️⃣ Я обработаю его и пришлю тебе без фона в формате PNG.\n"
        "3️⃣ Используй полученное изображение в своих проектах!\n\n"
        "⚠️ Чем контрастнее объект на фоне, тем лучше результат."
    )

# Обработчик изображений
@dp.message(lambda message: message.photo)
async def remove_bg(message: types.Message):
    photo = message.photo[-1]
    photo_bytes = BytesIO()
    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path, destination=photo_bytes)   

    # Открываем изображение и обрабатываем (твой код тут)
    input_image = Image.open(photo_bytes)
    output_image = remove(input_image)  # Используем rembg для удаления фона

    output_path = "no_bg.png"
    output_image.save(output_path, format="PNG")  # Сохраняем с прозрачным фоном

    # Отправляем как файл, чтобы не сжималось
    await message.answer_document(document=FSInputFile(output_path), caption="✅ Вот изображение без фона!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())