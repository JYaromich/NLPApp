from ntpath import join
import os
from telegram.update import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv
from e_dostavks_parse import CategoryParse

load_dotenv()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(os.getenv('HELLO_TEXT'))


def _product_instance(item: str):
    start_url = 'https://e-dostavka.by/search'

    return CategoryParse(
        start_url=start_url,
        search_item=item
    ).run()


def run(update: Update, context: CallbackContext):
    rubrics = _product_instance(update.message.text)
    print(1)


if __name__ == '__main__':
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, run))

    updater.start_polling()
    updater.idle()
