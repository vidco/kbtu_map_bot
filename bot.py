import ctypes
from time import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '1108472031:AAHdZGhDLe5IqCXfpqeR4ibA2nN04lz4r64'

lib = ctypes.cdll.LoadLibrary('./back/qwe.so')


def start(update, context):
    update.message.reply_text('Hi!')


def echo(update, context):
    _start = time()
    nums = update.message.text.split('+')
    a, b = int(nums[0]), int(nums[1])
    update.message.reply_text(str(lib.SampleAddInt(a, b)))
    update.message.reply_text(str(a+b))
    print(time() - _start)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
