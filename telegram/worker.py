# -*- coding: utf-8 -*-
from config import commands
from telegram.processors import TelegramProcessor


class TelegramWorker(TelegramProcessor):
    def process_messages(self):
        for message in self.check_new_messages():
            # Process high-level events:
            # 1. Adding new user by invite code
            # 2. Ignore message if it was received from non-authorized iser
            # 3. Try to enter code from field user
            if self.process_new_user(message):
                continue

            command = self.extract_command(message).lower()
            # region User commands:
            if command == commands.info:
                self._admin_command(message, self.dummy)
            elif command == commands.add_admin:
                self._admin_command(message, self.do_add_admin)
            elif command == commands.delete_admin:
                self._admin_command(message, self.do_delete_admin)
            elif command == commands.clean_admin:
                self._admin_command(message, self.do_cleanadmin)
            elif command == commands.stop:
                self._admin_command(message, self.do_stop)
