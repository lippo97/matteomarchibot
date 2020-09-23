# -*- coding: utf-8 -*-
import os
import telegram
import time
import logging
from telegram import Update
from telegram.ext import CommandHandler, Updater, CallbackContext, JobQueue

from .blocking_scheduler import BlockingScheduler
from .i18n import t
from .logger import logger
from .emoji import green_circle, red_circle

scheduler = BlockingScheduler()

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(t('app.startup_message'))

def start(update: Update, context: CallbackContext):
    def say_hi():
        update.message.reply_text('Messaggio schedulato')
    if 'jobs' not in context.chat_data:
        job = scheduler.every(5).seconds.do(say_hi)
        update.message.reply_text('Bot enabled.')
        logger.info('Scheduled message for {}'.format(update.message.from_user.name))
        context.chat_data['jobs'] = [job]
    else:
        update.message.reply_text('Bot already running in this chat.')

def stop(update: Update, context: CallbackContext):
    if 'jobs' in context.chat_data:
        for job in context.chat_data['jobs']:
            scheduler.cancel_job(job)
        update.message.reply_text('Bot disabled.')
        logger.info('Removed scheduled messagesfor {}'.format(update.message.from_user.name))
        del context.chat_data['jobs']
    else:
        update.message.reply_text('Bot isn\'t running.')

def status(update: Update, context: CallbackContext):
    if 'jobs' in context.chat_data:
        update.message.reply_text('Status: {}'.format(green_circle))
    else:
        update.message.reply_text('Status: {}'.format(red_circle))


def main():
    LOGIN_TOKEN = os.getenv('LOGIN_TOKEN')

    updater = Updater(token=LOGIN_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("status", status, pass_chat_data=True))
    dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))

    # Start polling in a different thread
    updater.start_polling()
    # Run the scheduler in the current thread
    scheduler.idle()

    # Leave application
    logger.info('Stopping updater thread...')
    updater.stop()
    logger.info('Done!')

if __name__ == "__main__":
    main()
