from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton
from ntpath import join
import os
from telegram.update import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv
from e_dostavks_parse import CategoryParse, ItemsParse

load_dotenv()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(os.getenv('HELLO_TEXT'))


def _get_category(item: str, url: str) -> dict:
    return CategoryParse(
        start_url=url,
        search_item=item
    ).run()


def get_rubrics_inline_keyboard(rubrics: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=rubric,
                               callback_data=str(
                                   {'name': rubrics['name'][i],
                                    'value': rubrics['value'][i]}
                               ))]
         for i, rubric in enumerate(rubrics['title'])]
    )


RUBRIC_TEXT = 'Выберите категорию товара:'
START_URL = 'https://e-dostavka.by/search'


def _product_instance(update: Update, context: CallbackContext):

    rubrics = _get_category(update.message.text, START_URL)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=RUBRIC_TEXT,
        reply_markup=get_rubrics_inline_keyboard(rubrics)
    )


def rubric_callback_handler(update: Update, context: CallbackContext):
    print(1)
    # eval(update.callback_query.data)
    # ItemsParse(
    #     start_url=START_URL,
    #     search_item=
    # )


def run(update: Update, context: CallbackContext):
    _product_instance(update, context)
    print(1)


if __name__ == '__main__':
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, run))
    dispatcher.add_handler(CallbackQueryHandler(rubric_callback_handler))

    updater.start_polling()
    updater.idle()
