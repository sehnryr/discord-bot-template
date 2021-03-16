# !/usr/bin/env python3

import configparser
import os
import logging
import logging.config
from typing import Iterator

import discord
from discord.ext import commands

DEFAULT_CONFIG_FILE: str = "bot.cfg"
CURRENT_DIRECTORY: str = os.getcwd()


class Bot(commands.Bot):
    def __init__(self, *args) -> None:
        config = self.get_config()

        self.token = config["discord"].get("token")
        self.prefix = config["discord"].get("prefix").split()
        self.description = config["discord"].get("description")
        self.supression_delay = config["discord"].getint("supression_delay")

        self._cogs_dir = config["discord"].get("cogs_dir")
        self._extensions = self.get_extensions()

        self.logger = self.get_logger(config=config)

        super().__init__(
            command_prefix=self.prefix,
            description=self.description,
            *args,
        )

        self.load_extensions()

    @classmethod
    def init(cls, token=None) -> None:
        bot = cls()
        token = token or bot.token

        try:
            bot.run(token)
        except Exception as e:
            bot.logger.warning(e)

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as: {self.user.name} - {self.user.id}")
        self.logger.info(f"Discord.py Version: {discord.__version__}")
        self.logger.info("Successfully logged in and booted...!")

        await self.change_presence(activity=discord.Game(name=f"{self.prefix}help"))

    async def on_command_error(self, context, e) -> None:
        await context.message.delete()
        await context.send(content=f"`{type(e).__name__}`: {e}", delete_after=self.supression_delay)
        self.logger.error(f"{type(e).__name__}: {e}: Command '{context.message.content.split()[0][1:]}'")

    async def on_error(self, event_method, *args, **kwargs) -> None:
        self.logger.error(f"{''.join(traceback.format_exception(*sys.exc_info()))}")

    def get_logger(self, config: configparser.ConfigParser) -> logging.Logger:
        logger_config = config["logging"]

        if logger_config.get("logs_dir") not in os.listdir():
            os.mkdir(path=logger_config.get("logs_dir"))

        formatter_config = config["logging.formatter"]
        handler_config = config["logging.file_handler"]

        logger = logging.getLogger(__name__)
        logger.setLevel(level=logger_config.getint("logger_level"))

        formatter = logging.Formatter(
            fmt=formatter_config.get("fmt"),
            datefmt=formatter_config.get("datefmt"),
            style="{",
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=stream_handler)

        handlers = {
            "FileHandler": logging.FileHandler,
            "RotatingFileHandler": logging.handlers.RotatingFileHandler,
            "TimedRotatingFileHandler": logging.handlers.TimedRotatingFileHandler,
        }
        handler_config_dict = dict()
        for key in handler_config.keys():
            if key in ["maxBytes", "backupCount", "interval"]:
                value = handler_config.getint(key)
            elif key in ["delay", "utc"]:
                value = handler_config.getboolean(key)
            else:
                value = handler_config.get(key)

            handler_config_dict[key] = value

        file_handler = handlers[logger_config.get("file_handler_type")](**handler_config_dict)
        file_handler.setLevel(logger_config.getint("file_handler_level"))
        file_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=file_handler)

        return logger

    def get_extensions(self) -> Iterator[str]:
        if self._cogs_dir not in os.listdir():
            os.mkdir(path=self._cogs_dir)

        return map(
            lambda filename: filename.replace(".py", ""),
            filter(
                lambda filename: filename.endswith(".py"),
                os.listdir(self._cogs_dir),
            ),
        )

    def load_extensions(self, cogs=None) -> None:
        for extension in cogs or self._extensions:
            try:
                self.load_extension(f"{self._cogs_dir}.{extension}")
                self.logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                self.logger.error(f"{type(e).__name__}: {e}")

    def get_config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser(
            comment_prefixes=None,
            interpolation=configparser.ExtendedInterpolation(),
        )
        config.optionxform = str

        if DEFAULT_CONFIG_FILE in os.listdir():
            config.read(DEFAULT_CONFIG_FILE)
            return config
        else:
            return self.create_config_file()

    def create_config_file(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=None,
            interpolation=configparser.ExtendedInterpolation(),
        )
        config.optionxform = str

        config["discord"] = {
            "prefix": "!",
            "token": "SECRET_TOKEN_HERE",
            "description": "Bot created with a template ",
            "supression_delay": 3,
            "cogs_dir": "cogs",
        }

        config["logging"] = {
            "logs_dir": "logs",
            "logger_level": logging.INFO,
            "stream_handler": True,
            "file_handler_type": "TimedRotatingFileHandler",
            "file_handler_level": "${logging:logger_level}",
        }

        # use a %% to escape the % sign (% is the only character that needs to be escaped)
        config["logging.formatter"] = {
            "fmt": "[{asctime}] [{levelname}] [{name}] : {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }

        config["logging.file_handler"] = {
            "filename": "${logging:logs_dir}/latest.log",
            "when": "midnight",
            "backupCount": 10,
            "utc": False,
        }

        with open(DEFAULT_CONFIG_FILE, "w+") as configfile:
            config.write(configfile)

        return config


if __name__ == "__main__":
    Bot.init()
