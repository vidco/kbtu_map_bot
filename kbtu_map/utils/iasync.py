from telegram.ext.dispatcher import run_async


@run_async
def send_photo(update, bot, images):
    for image in images:
        bot.send_photo(chat_id=update.message.chat_id, photo=image)
