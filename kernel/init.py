import os, logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

def init():
    load_dotenv()
    TOKEN = os.getenv('TOKEN') 

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token(TOKEN).build()
    application.run_polling()