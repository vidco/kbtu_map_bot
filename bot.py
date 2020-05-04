from PIL import Image, ImageDraw2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from back import Graph
from utils.timer import timing_decorator
from utils.coord import COORD

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'        # Bot token
G = Graph()                                                     # Graph of KBTU with all nodes (locations)
FIRST, SECOND = range(2)                                        # States of Conversation for path finding
NUMBER_REGEX = '^[0-9]+$'                                       # Regex for numbers (node numbers)


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
    Ask for final location
    """
    context.user_data['from'] = int(update.message.text)

    update.message.reply_text('Where you want to go?')

    return SECOND


@timing_decorator
def path(update, context):
    """
    Calculate and return path between two locations
    """
    node_from = context.user_data['from']
    node_to = int(update.message.text)

    minimal_path = G.mindist(node_from, node_to)

    im = Image.open("images/qwe.png")
    d = ImageDraw2.Draw(im)

    pen = ImageDraw2.Pen(color="red")
    nodes = []

    for node in minimal_path:
        obj = COORD[node]
        x = obj['x']
        y = obj['y']

        nodes.append((x, y))

    d.line(nodes, pen)
    im.save("drawn_grid.png")

    update.message.reply_text(' -> '.join(str(COORD[node]['number']) for node in minimal_path))

    return ConversationHandler.END


def cancel(update, context):
    """
    Cancel Conversation for path finding and deletes 'from' location if exists
    """
    if 'from' in context.user_data:
        del context.user_data['from']

    update.message.reply_text('Canceled')


def main():
    updater = Updater(TOKEN, use_context=True)

    # Register /start command
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Register Conversation Handler with /path and /cancel commands
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('path', path_from)],
            states={
                FIRST: [MessageHandler(Filters.regex(NUMBER_REGEX), path_to)],
                SECOND: [MessageHandler(Filters.regex(NUMBER_REGEX), path)]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
