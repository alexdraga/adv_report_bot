# -*- coding: utf-8 -*-s
from config import bot_settings
from config.dictionary import CommonMessages, UserMessages, BotSystemMessages, CommandMessages
from telegram.abstract_processors import AbstractProcessors


class TelegramProcessor(AbstractProcessors):
    def dummy(self, message):
        self.send_message(message["from_id"], "dummy")

    def do_add_admin(self, message):
        if len(message["text"].split()) > 1:
            admin_to_add = message["text"].split()[1]
            if not admin_to_add.isdigit():
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                if bot_settings.is_admin(int(admin_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    bot_settings.add_admin_id(int(admin_to_add))
                    self.admin_message(
                        UserMessages.NEW_ADMIN_WAS_ADDED.format(
                            user_id=admin_to_add,
                            nickname=self.get_username(admin_to_add)))
                    self.send_message(admin_to_add, UserMessages.HELLO_NEW_ADMIN)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_delete_admin(self, message):
        if len(bot_settings.admin_ids) == 1:
            self.answer_message(message, UserMessages.CANNOT_DELETE_ADMIN)
        else:
            admin_to_delete = self.get_new_value(
                message,
                UserMessages.DELETE_USER_ID.format(
                    current_ids=self.get_usernames(bot_settings.admin_ids)))
            if not admin_to_delete.isdigit() or int(admin_to_delete) not in bot_settings.admin_ids:
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                bot_settings.delete_admin_id(int(admin_to_delete))
                self.answer_message(message, UserMessages.USER_DELETED)

    def do_cleanadmin(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            bot_settings.clean_admins()
            self.answer_message(message, BotSystemMessages.ADMIN_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_stop(self, message):
        self.answer_message(message, CommonMessages.BYE)
        self.stopped = True

    def process_new_user(self, message):
        passphrase = message["text"]
        from_id = message["from_id"]
        if passphrase == bot_settings.admin_passphrase:
            if from_id in bot_settings.admin_ids:
                return False
            else:
                bot_settings.add_admin_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_ADMIN)
                self.admin_message(
                    UserMessages.NEW_ADMIN_WAS_ADDED.format(user_id=from_id,
                                                            nickname=self.get_username(from_id)))
                return True
