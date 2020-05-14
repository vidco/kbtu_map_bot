import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from kbtu_map.db import Database
from kbtu_map.graph import Graph
from kbtu_map.settings import USERS_PATH, GRAPH_PATH
from kbtu_map.utils import ACTIONS

USERS = Database(USERS_PATH)                             # Users database
GRAPH = Graph(GRAPH_PATH)                                # Graph with node information

FIRST = range(1)

LOG = logging.getLogger('level')


def path_cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    language = get_user_language(update, context)

    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text(ACTIONS.get('cancel').get(language))
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


def change_level(update, context):
    """

    """
    language = get_user_language(update, context)
    custom_keyboard = [['0', '1', '2', '3']]
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=ACTIONS.get('ask_level').get(language),
                             reply_markup=ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True))

    return FIRST


def changing_level(update, context):
    """

    """
    text = update.message.text
    telegram_id = update.message.from_user.id
    USERS.update_user_level(telegram_id, text)
    language = USERS.select_language_by_telegram_id(telegram_id)

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=ACTIONS.get('changed_level').get(language),
                             reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def as_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('level', change_level)],
        states={
            FIRST: [MessageHandler(Filters.regex('^[0-3]{1}$'), changing_level)],
        },
        fallbacks=[CommandHandler('cancel', path_cancel)]
    )
