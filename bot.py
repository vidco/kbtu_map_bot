from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from graph import Graph, Path
from utils import timing_decorator, draw

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'        # Bot token
UPDATER = Updater(TOKEN, use_context=True)                      # Main Bot object
PATH = Path()                                                   # Graph for calculating minimal path
GRAPH = Graph()                                                 # Graph with node information
FIRST, SECOND = range(2)                                        # States of Conversation for path finding


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
    node_id = GRAPH.check_by_name(update.message.text)

    if node_id:
        context.user_data['from'] = node_id
        update.message.reply_text('Where you want to go?')

        return SECOND

    else:
        update.message.reply_text('Not found. Try again')

        return FIRST


@timing_decorator
def path(update, context):
    """
    Check if node exists, if not return to SECOND
    Calculate and return path between two locations
    """
    id_to = GRAPH.check_by_name(update.message.text)

    if not id_to:
        update.message.reply_text('Not found. Try again')

        return SECOND

    minimal_path = PATH.minimum_path(context.user_data.get('from'), id_to)

    print(minimal_path)
    print(GRAPH.get_delimited_path(minimal_path))

    path_coordinates = GRAPH.get_delimited_path(minimal_path)

    # Draw on template image nodes
    images = draw(path_coordinates)

    update.message.reply_text(GRAPH.path(minimal_path))

    for image in images:
        UPDATER.bot.send_photo(chat_id=update.message.chat_id, photo=image)

    return ConversationHandler.END


def cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text('Canceled')


def main():
    # Register /start command
    UPDATER.dispatcher.add_handler(CommandHandler("start", start))

    # Register Conversation Handler with /path and /cancel commands
    UPDATER.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('path', path_from)],
            states={
                FIRST: [MessageHandler(Filters.text, path_to)],
                SECOND: [MessageHandler(Filters.text, path)]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
    )

    UPDATER.start_polling()
    UPDATER.idle()


if __name__ == '__main__':
    main()
