import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from kbtu_map.db import Database
from kbtu_map.graph import Graph
from kbtu_map.settings import USERS_PATH, GRAPH_PATH, SIDE_DELTA
from kbtu_map.utils import ACTIONS, draw
from kbtu_map.utils.iasync import send_photo

USERS = Database(USERS_PATH)
GRAPH = Graph(GRAPH_PATH)

FLOOR_FROM, FLOOR_TO = range(2)

LOG = logging.getLogger('floor')


def floor_from(update, context):
    """
    Ask for initial location
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    update.message.reply_text(ACTIONS.get('ask_location').get(language))

    return FLOOR_FROM


def floor_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text(ERRORS.get('not_found').get(language))

        return FLOOR_FROM

    else:
        context.user_data['from'] = node_id
        update.message.reply_text(ACTIONS.get('ask_floor').get(language))

        return FLOOR_TO


def floor(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

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

    send_photo(update, context.bot, images)

    return ConversationHandler.END


def floor_cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text(ACTIONS.get('cancel').get(language))
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


def as_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('floor', floor_from)],
        states={
            FLOOR_FROM: [MessageHandler(Filters.regex('^[0-9]{3}$'), floor_to)],
            FLOOR_TO: [MessageHandler(Filters.regex('^[0-9]{1}$'), floor)]
        },
        fallbacks=[CommandHandler('cancel', floor_cancel)]
    )
