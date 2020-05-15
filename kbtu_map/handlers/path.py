import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from kbtu_map.db import Database
from kbtu_map.graph import Map
from kbtu_map.settings import SIDE_DELTA
from kbtu_map.utils import ACTIONS, draw, describe
from kbtu_map.utils.iasync import send_photo
from kbtu_map.utils.timer import timing_decorator

USERS = Database.get_instance()
GRAPH = Map.get_instance()

PATH_FROM, PATH_TO = range(2)

LOG = logging.getLogger('path')


def path_from(update, context):
    """
    Ask for initial location
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

    update.message.reply_text(ACTIONS.get('ask_location').get(language))

    return PATH_FROM


def path_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)

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
    language = USERS.select_language_by_telegram_id(update.message.from_user.id)
    level = USERS.select_level_by_telegram_id(update.message.from_user.id)

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

    send_photo(update, context.bot, images)

    return ConversationHandler.END


def path_cancel(update, context):
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
        entry_points=[CommandHandler('path', path_from)],
        states={
            PATH_FROM: [MessageHandler(Filters.regex('^[0-9]{3}$'), path_to)],
            PATH_TO: [MessageHandler(Filters.regex('^[0-9]{3}$'), path)]
        },
        fallbacks=[CommandHandler('cancel', path_cancel)]
    )
