import os
import telegram
from telegram.ext import CommandHandler, Updater, CallbackContext

def start(update, context: CallbackContext):
    update.message.reply_text('Ciao! Sono {} in beta'.format(context.bot.name))

def main():
    LOGIN_TOKEN = os.getenv('LOGIN_TOKEN')

    updater = Updater(token=LOGIN_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
