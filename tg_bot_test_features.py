from telegram.ext import CallbackQueryHandler  # Обработчик нажатия на кнопку
from telegram import InlineKeyboardMarkup  # Вся клавиатура
from telegram import InlineKeyboardButton  # одна клавиша
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram import Update, Bot
from telegram.ext import Updater


updater = Updater(token='5777519924:AAEUd5TMiOwG7R6nxvrQIvGUnVm0RAY1cps')
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def get_inline_keyboard():
    keyboard = [

        InlineKeyboardButton(
            text='button_1', callback_data='callback_button_left'),
        InlineKeyboardButton(
            text='button_2', callback_data='callback_button_right')

    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    print(1)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
        reply_markup=get_inline_keyboard())


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
button_handler = CallbackQueryHandler(
    callback=keyboard_callback_handler, pass_chat_data=True)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(button_handler)


def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()
