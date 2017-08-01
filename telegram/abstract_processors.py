# -*- coding: utf-8 -*-
from config import bot_settings
from telegram.driver import TelegramDriver


class AbstractProcessors(TelegramDriver):
    stopped = False

    def __init__(self):
        super(AbstractProcessors, self).__init__()
        self._load_settings()

    def _reset(self):
        self.get_updates()
        bot_settings.paused = True
        self._load_settings()

    def _load_settings(self):
        pass

    def _admin_command(self, message, do_function):
        from_id = message["from_id"]
        if bot_settings.is_admin(from_id):
            do_function(message)
