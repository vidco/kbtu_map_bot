import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from kbtu_map.db import Database
from kbtu_map.graph import Graph
from kbtu_map.settings import USERS_PATH, GRAPH_PATH
from kbtu_map.utils import ACTIONS, flag, unflag, unflaggable

USERS = Database(USERS_PATH)                             # Users database
GRAPH = Graph(GRAPH_PATH)                                # Graph with node information

FIRST = range(1)

LOG = logging.getLogger('language')                                 # Main logger


def cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text(ACTIONS.get('cancel').get(language))
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


def change_language(update, context):
    """

    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)
    custom_keyboard = [[flag('us'), flag('kz'), flag('ru')]]
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=ACTIONS.get('ask_language').get(language),
                             reply_markup=ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True))

    return FIRST


def changing_language(update, context):
    """

    """
    if not unflaggable(update.message.text):
        return FIRST

    text = unflag(update.message.text)
    telegram_id = update.message.from_user.id
    USERS.update_user_language(telegram_id, text)
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=ACTIONS.get('changed_language').get(language),
                             reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def as_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('language', change_language)],
        states={
            FIRST: [MessageHandler(Filters.text, changing_language)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
