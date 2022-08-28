import os
from telegram.update import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(os.getenv('HELLO_TEXT'))


if __name__ == '__main__':
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
