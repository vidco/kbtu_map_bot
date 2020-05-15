from telegram.ext import CommandHandler

from kbtu_map.db import Database
from kbtu_map.settings import USERS_PATH
from kbtu_map.utils import ACTIONS

USERS = Database(USERS_PATH)


def help(update, context):
	language = USERS.select_language_by_telegram_id(update.message.from_user.id)
	update.message.reply_text(ACTIONS.get('help').get(language))


def as_handler():
	return CommandHandler('help', help)