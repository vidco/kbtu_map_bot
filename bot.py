from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.dispatcher import run_async

from graph import Graph
from utils import timing_decorator, draw

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'        # Bot token
GRAPH = Graph('graph/nodes.csv')                                # Graph with node information
FIRST, SECOND = range(2)                                        # States of Conversation for path finding
SIDE_DELTA = 10


def start(update, context):
    update.message.reply_text('Hello! I can find fastest path to any place in KBTU')


def path_from(update, context):
    """
    Ask for initial location
    """
    update.message.reply_text('Where are you?')

    return FIRST


def path_to(update, context):
    """
    Check if node exists, if not return to FIRST
    Then ask for final location
    """
    node_id = GRAPH.get_id_by_location(update.message.text)

    if node_id == -1:
        update.message.reply_text('Not found. Try again')

        return FIRST

    else:
        context.user_data['from'] = node_id
        update.message.reply_text('Where you want to go?')

        return SECOND


@timing_decorator
def path(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    id_to = GRAPH.get_id_by_location(update.message.text)

    if id_to == -1:
        update.message.reply_text('Not found. Try again')

        return SECOND

    minimal_path = GRAPH.get_min_dist(context.user_data.get('from'), id_to)

    print('path: ' + str(minimal_path))

    path_coordinates = GRAPH.get_path_on_floor(minimal_path, SIDE_DELTA)

    print('floor paths: ' + str(path_coordinates))

    images = draw(path_coordinates)

    update.message.reply_text(GRAPH.path_description(minimal_path))

    _send_photo_async(update, context.bot, images)

    return ConversationHandler.END


def cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text('Canceled')

    return ConversationHandler.END


@run_async
def _send_photo_async(update, bot, images):
    for image in images:
        bot.send_photo(chat_id=update.message.chat_id, photo=image)


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
                FIRST: [MessageHandler(Filters.regex('^[0-9]{3}$'), path_to)],
                SECOND: [MessageHandler(Filters.regex('^[0-9]{3}$'), path)]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
