from os import path

from config.bot_settings import BotSettingsConfig
from config.commands import CommandsConfig
from config.errors import ErrorsLog
from config.timeouts import TimeoutsConfig

bot_settings = BotSettingsConfig(path.join("yaml", "bot_settings.yaml"))
commands = CommandsConfig(path.join("yaml", "commands.yaml"))
errors_log = ErrorsLog(path.join("yaml", "errors_log.yaml"))
timeouts = TimeoutsConfig(path.join("yaml", "timeouts.yaml"))