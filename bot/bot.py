# -*- coding: utf-8 -*-
import os
import sys
import telegram
import time
import logging
from telegram import Update
from telegram.ext import CommandHandler, Updater, CallbackContext, JobQueue

from .scheduler import scheduler
from .i18n_conf import t
from .logger import logger
from .emoji import green_circle, red_circle
from .events import events
from .git import branch_name, remote_repo, version as repo_version
import yaml

JOBS = 'jobs'

def schedule_events(reply_text):
    events_with_callback = [(dt, lambda: reply_text(msg, parse_mode=telegram.ParseMode.HTML)) for dt, msg in events if not dt == None]
    jobs = scheduler.add_jobs(events_with_callback)
    return jobs

def _help(update: Update, context: CallbackContext):
    update.message.reply_text(t('app.info.help', name=context.bot.name))

def start(update: Update, context: CallbackContext):
    if JOBS not in context.chat_data:
        jobs = schedule_events(update.message.reply_text)
        update.message.reply_text(t('app.scheduling.enabled'))
        context.chat_data[JOBS] = jobs
        logger.info('Scheduled message for {}'.format(update.message.from_user.name))
    else:
        update.message.reply_text(t('app.scheduling.already_enabled'))

def stop(update: Update, context: CallbackContext):
    if JOBS in context.chat_data:
        for job in context.chat_data[JOBS]:
            job.remove()
        update.message.reply_text(t('app.scheduling.disabled'))
        logger.info('Removed scheduled messages for {}'.format(update.message.from_user.name))
        del context.chat_data[JOBS]
    else:
        update.message.reply_text(t('app.scheduling.already_disabled'))

def status(update: Update, context: CallbackContext):
    status = green_circle if JOBS in context.chat_data else red_circle
    update.message.reply_text(t('app.scheduling.status', status=status))

def version(update: Update, context: CallbackContext):
    repo = {
        'name': context.bot.name,
        'version': repo_version,
        'branch_name': branch_name,
        'remote_repo': remote_repo,
    }
    update.message.reply_text(t('app.info.version', **repo), parse_mode=telegram.ParseMode.HTML)

def main():
    LOGIN_TOKEN = os.getenv('LOGIN_TOKEN')
    if LOGIN_TOKEN in (None, 'INSERT_TOKEN_HERE'):
        print('Environment variable LOGIN_TOKEN not found.', file=sys.stderr)
        exit(1)

    updater = Updater(token=LOGIN_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("status", status, pass_chat_data=True))
    dp.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))
    dp.add_handler(CommandHandler("version", version))

    updater.start_polling()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info('Received stop signal.')
    finally:
        logger.info('Stopping updater thread...')
        updater.stop()

    # Leave application
    logger.info('Done!')

if __name__ == "__main__":
    main()
