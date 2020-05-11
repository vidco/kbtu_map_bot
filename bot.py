import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.dispatcher import run_async

from graph import Graph
from utils import timing_decorator, draw, describe

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'        # Bot token
GRAPH = Graph('graph/nodes.csv')                                # Graph with node information
PATH_FROM, PATH_TO = range(2)                                   # States of Conversation for path finding
FLOOR_FROM, FLOOR_TO = range(2)                                 # States of Conversation for path finding
SIDE_DELTA = 10                                                 # Distance between roads and
logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s] - %(message)s', level=logging.INFO)
LOG = logging.getLogger('main')                                 # Main logger


def start(update, context):
    update.message.reply_text('Hello! I can find fastest path to any place in KBTU')


def path_from(update, context):
    """
    Ask for initial location
    """
    update.message.reply_text('Where are you?')

    return PATH_FROM


def path_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text('Not found. Try again')

        return PATH_FROM

    else:
        context.user_data['from'] = node_id
        update.message.reply_text('Where you want to go?')

        return PATH_TO


@timing_decorator
def path(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    id_to = GRAPH.get_id_by_location(update.message.text)

    if id_to == -1:
        update.message.reply_text('Not found. Try again')

        return PATH_TO

    minimal_path = GRAPH.get_min_dist(context.user_data.get('from'), id_to)

    LOG.info('full path: %s', minimal_path)

    path_coordinates = GRAPH.get_path_on_floor(minimal_path, SIDE_DELTA)

    LOG.info('floor path: %s', path_coordinates)

    images = draw(path_coordinates)

    update.message.reply_text(describe(GRAPH.path_description(minimal_path)))

    _send_photo_async(update, context.bot, images)

    return ConversationHandler.END


def path_cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text('Canceled')
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


def floor_from(update, context):
    """
    Ask for initial location
    """
    update.message.reply_text('Where are you?')

    return FLOOR_FROM


def floor_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text('Not found. Try again')

        return FLOOR_FROM

    else:
        context.user_data['from'] = node_id
        update.message.reply_text('What floor do you want to go to?')

        return FLOOR_TO


@timing_decorator
def floor(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    message = update.message.text
    if not message.isnumeric():
        update.message.reply_text('Not valid floor')

        return FLOOR_TO

    _floor = int(message)

    if not GRAPH.is_valid_floor(_floor):
        update.message.reply_text('Not found. Try again')

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
    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text('Canceled')
    LOG.info('Update "%s" canceled', update)

    return ConversationHandler.END


@run_async
def _send_photo_async(update, bot, images):
    for image in images:
        bot.send_photo(chat_id=update.message.chat_id, photo=image)


def error(update, context):
    """Log Errors caused by Updates."""
    LOG.error('Update "%s" caused error "%s"', update, context.error)


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

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
