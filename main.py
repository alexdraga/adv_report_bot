# -*- coding: utf-8 -*-
from time import sleep
from traceback import format_exc

from config import errors_log, bot_settings
from telegram.worker import TelegramWorker

bot = TelegramWorker()


while not bot.stopped:
    try:
        bot.process_messages()
        sleep(0.5)
    except Exception, e:
        bot.admin_message(format_exc())
        errors_log.log_error(format_exc())
