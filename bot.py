import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.dispatcher import run_async

from db import Database
from graph import Graph
from utils import timing_decorator, draw, describe, ACTIONS, ERRORS, flag, unflag, unflaggable

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'        # Bot token
GRAPH = Graph('graph/nodes.csv')                                # Graph with node information
USERS = Database('users.db')                             # Users database
PATH_FROM, PATH_TO = range(2)                                   # States of Conversation for path finding
FLOOR_FROM, FLOOR_TO = range(2)                                 # States of Conversation for path finding
FIRST = range(1)
SIDE_DELTA = 10                                                 # Distance between roads and
logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s] - %(message)s', level=logging.INFO)
LOG = logging.getLogger('main')                                 # Main logger


def get_user_language(update, context):
    user = update.message.from_user
    return USERS.select_language_by_telegram_id(user.id)


def get_user_level(update, context):
    user = update.message.from_user
    return USERS.select_level_by_telegram_id(user.id)


def start(update, context):
    user = update.message.from_user
    telegram_id = user.id

    if not USERS.user_exists(telegram_id):
        USERS.create_user(telegram_id)

    language = USERS.select_language_by_telegram_id(telegram_id)
    update.message.reply_text(ACTIONS.get('greetings').get(language))


def change_language(update, context):
    """

    """
    language = get_user_language(update, context)
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
    language = USERS.select_language_by_telegram_id(telegram_id)

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=ACTIONS.get('changed_language').get(language),
                             reply_markup=ReplyKeyboardRemove())

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


def path_from(update, context):
    """
    Ask for initial location
    """
    language = get_user_language(update, context)

    update.message.reply_text(ACTIONS.get('ask_location').get(language))

    return PATH_FROM


def path_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    language = get_user_language(update, context)

    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text(ERRORS.get('not_found').get(language))

        return PATH_FROM

    else:
        context.user_data['from'] = node_id
        update.message.reply_text(ACTIONS.get('ask_destination').get(language))

        return PATH_TO


@timing_decorator
def path(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    language = get_user_language(update, context)
    level = get_user_level(update, context)

    id_to = GRAPH.get_id_by_location(update.message.text)

    if id_to == -1:
        update.message.reply_text(ERRORS.get('not_found').get(language))

        return PATH_TO

    minimal_path = GRAPH.get_min_dist(context.user_data.get('from'), id_to)

    LOG.info('full path: %s', minimal_path)

    path_coordinates = GRAPH.get_path_on_floor(minimal_path, SIDE_DELTA)

    LOG.info('floor path: %s', path_coordinates)

    images = draw(path_coordinates)

    message = describe(GRAPH.path_description(minimal_path), language, level)

    if len(message) > 0:
        update.message.reply_text(message)

    _send_photo_async(update, context.bot, images)

    return ConversationHandler.END


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


def floor_from(update, context):
    """
    Ask for initial location
    """
    language = get_user_language(update, context)

    update.message.reply_text(ACTIONS.get('ask_location').get(language))

    return FLOOR_FROM


def floor_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    language = get_user_language(update, context)

    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text(ERRORS.get('not_found').get(language))

        return FLOOR_FROM

    else:
        context.user_data['from'] = node_id
        update.message.reply_text(ACTIONS.get('ask_floor').get(language))

        return FLOOR_TO


@timing_decorator
def floor(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    language = get_user_language(update, context)

    message = update.message.text
    if not message.isnumeric():
        update.message.reply_text(ERRORS.get('invalid_floor').get(language))

        return FLOOR_TO

    _floor = int(message)

    if not GRAPH.is_valid_floor(_floor):
        update.message.reply_text(ERRORS.get('not_found').get(language))

        return FLOOR_TO

    minimal_path = GRAPH.get_min_dist_to_floor(context.user_data.get('from'), _floor)

    LOG.info('full path: %s', minimal_path)

    path_coordinates = GRAPH.get_path_on_floor(minimal_path, SIDE_DELTA)

    LOG.info('floor path: %s', path_coordinates)

    images = draw(path_coordinates)

    update.message.reply_text(GRAPH.path_description(minimal_path))

    _send_photo_async(update, context.bot, images)

    return ConversationHandler.END


def floor_cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    language = get_user_language(update, context)

    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text(ACTIONS.get('cancel').get(language))
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


@run_async
def _send_photo_async(update, bot, images):
    for image in images:
        bot.send_photo(chat_id=update.message.chat_id, photo=image)


def error(update, context):
    """Log Errors caused by Updates."""
    LOG.error(context.error)


def main():
    # Main Bot object
    updater = Updater(TOKEN, use_context=True)

    # Register /start command
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Register Conversation Handler with /path and /cancel commands
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('path', path_from)],
            states={
                PATH_FROM: [MessageHandler(Filters.regex('^[0-9]{3}$'), path_to)],
                PATH_TO: [MessageHandler(Filters.regex('^[0-9]{3}$'), path)]
            },
            fallbacks=[CommandHandler('cancel', path_cancel)]
        )
    )

    # Register Conversation Handler with /floor and /cancel commands
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('floor', floor_from)],
            states={
                FLOOR_FROM: [MessageHandler(Filters.regex('^[0-9]{3}$'), floor_to)],
                FLOOR_TO: [MessageHandler(Filters.regex('^[0-9]{1}$'), floor)]
            },
            fallbacks=[CommandHandler('cancel', floor_cancel)]
        )
    )

    # Register Conversation Handler with /language and /cancel commands
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('language', change_language)],
            states={
                FIRST: [MessageHandler(Filters.text, changing_language)],
            },
            fallbacks=[CommandHandler('cancel', path_cancel)]
        )
    )

    # Register Conversation Handler with /language and /cancel commands
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('level', change_level)],
            states={
                FIRST: [MessageHandler(Filters.regex('^[0-3]{1}$'), changing_level)],
            },
            fallbacks=[CommandHandler('cancel', path_cancel)]
        )
    )

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
