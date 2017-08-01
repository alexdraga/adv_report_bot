import base64

import msgpack

from base_config import BaseConfig


class BotSettingsConfig(BaseConfig):

    @property
    def bot_token(self):
        return self.config.get("bot", {}).get("token")

    @bot_token.setter
    def bot_token(self, value):
        self.config["bot"]["token"] = value
        self.save_config()

    @property
    def paused(self):
        return self.config.get("bot", {}).get("paused")

    @paused.setter
    def paused(self, value):
        self.config["bot"]["paused"] = value
        self.save_config()

    @property
    def updates_path(self):
        return self.config.get("bot", {}).get("updates-path")

    @property
    def users_path(self):
        return self.config.get("bot", {}).get("users-path")

    @property
    def send_document_path(self):
        return self.config.get("bot", {}).get("send-document-path")

    @property
    def send_message_path(self):
        return self.config.get("bot", {}).get("send-message-path")

    @property
    def admin_passphrase(self):
        raw = self.config.get("bot", {}).get("admin_passphrase")
        return base64.decodestring(raw)

    @admin_passphrase.setter
    def admin_passphrase(self, passphrase):
        self.config["bot"]["admin_passphrase"] = base64.encodestring(passphrase)
        self.save_config()

    @property
    def admin_ids(self):
        raw = self.config.get("bot", {}).get("obfuscation_id")
        if raw is None:
            return []
        decoded = base64.decodestring(raw)
        admins = msgpack.loads(decoded)
        return admins

    @admin_ids.setter
    def admin_ids(self, ids):
        self.config["bot"]["obfuscation_id"] = ids
        self.save_config()

    def add_admin_id(self, admin_id):
        admin_ids = self.admin_ids + [admin_id]
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def delete_admin_id(self, admin_id):
        admin_ids = self.admin_ids[:]
        admin_ids.remove(admin_id)
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def clean_admins(self):
        encoded = msgpack.dumps([])
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def is_admin(self, from_id):
        return from_id in self.admin_ids
