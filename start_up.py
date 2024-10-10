import io
import logging
from telegram import Update, InputSticker
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from settings import *
from PIL import Image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def create_sticker_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_dict = update.to_dict()

    sticker_file_id = update.message.photo[-1].file_id  

    file = await context.bot.get_file(sticker_file_id)
    photo_bytes = await file.download_as_bytearray()
    
    # Открываем изображение с помощью PIL
    image = Image.open(io.BytesIO(photo_bytes))
    
    # Обрабатываем изображение (например, изменяем размер)
    image = image.resize((512, 512))  # Стикеры обычно имеют размер 512x512
    
    # Сохраняем обработанное изображение во временный файл
    temp_file = io.BytesIO()
    image.save(temp_file, format='PNG')
    temp_file.seek(0)

    input_sticker = InputSticker(
        sticker=temp_file,
        emoji_list=["😀"],  # Список эмодзи, ассоциированных со стикером
        format='static'
    )   

    new_pack = await context.bot.create_new_sticker_set(
            user_id=update.effective_chat.id,
            name=f'jestko_testim_maxima_by_{context.bot.username}',
            title='Жестко тестим Максима',
            stickers=[input_sticker]
        )
    
    pack_link = f"https://t.me/addstickers/jestko_testim_maxima_by_{context.bot.username}"

    await update.message.reply_text(f"Стикер-пак успешно создан! Вот ссылка на него:\n{pack_link}")
    


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    sticker_set_create_handler = MessageHandler(filters.PHOTO, create_sticker_set)
    application.add_handler(start_handler)
    application.add_handler(sticker_set_create_handler)
    
    application.run_polling()