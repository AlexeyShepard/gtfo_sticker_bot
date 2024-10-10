from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from kernel.base_handler import *

class start_handler(base_handler):

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
    def make(self):
        return CommandHandler('start', self.start)

    
    