# -*- coding: utf-8 -*-
import os
import telegram
import time
import logging
from telegram import Update
from telegram.ext import CommandHandler, Updater, CallbackContext, JobQueue

from .blocking_scheduler import scheduler
from .i18n_conf import t
from .logger import logger
from .emoji import green_circle, red_circle

JOBS = 'jobs'

def hello(update: Update, context: CallbackContext):
    update.message.reply_text(t('app.startup_message'))

def start(update: Update, context: CallbackContext):
    def say_hi():
        update.message.reply_text('Messaggio schedulato')
    if JOBS not in context.chat_data:
        job = scheduler.every(5).seconds.do(say_hi)
        update.message.reply_text(t('app.scheduling.enabled'))
        logger.info('Scheduled message for {}'.format(update.message.from_user.name))
        context.chat_data[JOBS] = [job]
    else:
        update.message.reply_text(t('app.scheduling.already_enabled'))

def stop(update: Update, context: CallbackContext):
    if JOBS in context.chat_data:
        for job in context.chat_data[JOBS]:
            scheduler.cancel_job(job)
        update.message.reply_text(t('app.scheduling.disabled'))
        logger.info('Removed scheduled messages for {}'.format(update.message.from_user.name))
        del context.chat_data[JOBS]
    else:
        update.message.reply_text(t('app.scheduling.already_disabled'))

def status(update: Update, context: CallbackContext):
    status = green_circle if JOBS in context.chat_data else red_circle
    update.message.reply_text(t('app.scheduling.status', status=status))

def main():
    LOGIN_TOKEN = os.getenv('LOGIN_TOKEN')

    updater = Updater(token=LOGIN_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("status", status, pass_chat_data=True))
    dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))

    logger.info('Starting the polling thread...')
    # Start polling in a different thread
    updater.start_polling()
    # Run the scheduler in the current thread
    scheduler.run_blocking()

    # Leave application
    logger.info('Stopping updater thread...')
    updater.stop()
    logger.info('Done!')

if __name__ == "__main__":
    main()
