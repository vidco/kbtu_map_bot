import logging

from telegram.ext import Updater, CommandHandler

from kbtu_map.db import Database
from kbtu_map.handlers import floor, path, language, level
from kbtu_map.settings import USERS_PATH, TOKEN
from kbtu_map.utils import ACTIONS

USERS = Database(USERS_PATH)
LOG = logging.getLogger('main')


def start(update, context):
    user = update.message.from_user
    telegram_id = user.id

    if not USERS.user_exists(telegram_id):
        USERS.create_user(telegram_id)

    lang = USERS.select_language_by_telegram_id(telegram_id)
    update.message.reply_text(ACTIONS.get('greetings').get(lang))


def error(update, context):
    LOG.error(context.error)


def main():
    # Main Bot object
    updater = Updater(TOKEN, use_context=True)

    # Register /start command
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Register Conversation Handler with /path and /cancel commands
    updater.dispatcher.add_handler(path.as_handler())

    # Register Conversation Handler with /floor and /cancel commands
    updater.dispatcher.add_handler(floor.as_handler())

    # Register Conversation Handler with /language and /cancel commands
    updater.dispatcher.add_handler(language.as_handler())

    # Register Conversation Handler with /level and /cancel commands
    updater.dispatcher.add_handler(level.as_handler())

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
