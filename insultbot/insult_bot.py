# insult_bot.py
import random

import discord
import os
from pprint import pprint

from . import __version__
from .insult_api import InsultApi
from discord.ext import commands


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_insult_api", "_recently_insulted"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        self._insult_api = InsultApi()
        self._recently_insulted = False

    @property
    def insult_api(self):
        return self._insult_api

    @property
    def recently_insulted(self):
        return self._recently_insulted

    @recently_insulted.setter
    def recently_insulted(self, value: bool):
        self._recently_insulted = value

    async def on_ready(self):
        guilds = self.guilds
        print(f"\n{self.user} v{__version__} has loaded in {len(guilds)} guild(s):")
        pprint(guilds)
        print()

    def talk_back(self, message: discord.Message) -> bool:
        """
        Decides if a user is talking back to the bot

        :param message: Message to analyze
        :return: If the bot has determined the user is talking back
        """
        if message.reference is not None and message.reference.resolved.author == self.user:
            print("Bot detected a reply")
            return True
        if not self._recently_insulted:
            # no print statement here, this would clog the logs
            return False
        content = message.content.lower()
        triggers = ["you", "yourself", "youre", "you're", "your", "yours"]
        for trigger in triggers:
            if trigger in content:
                print("Bot detected a trigger word")
                return True
        return False

    def generate_insult(self, user: discord.User) -> str:
        """
        Generates and formats an insult from the API

        :param user: User to insult
        :return: Formatted insult
        """
        user_tag = f"<@{user.id}>"  # tags the user
        # 1 in 9 chance to just flip them off
        if not random.randint(1, 9) % 9:
            print("Bot will flip the bird")
            return user_tag + " 🖕"
        insult = self._insult_api.get_insult()
        insult = insult.replace("{user}", user_tag) if "{user}" in insult \
            else user_tag + " " + insult
        print("Bot generated insult with following data:")
        pprint({"user": {"name": f"{user.name}#{user.discriminator}", "id": user.id}, "insult": insult})
        return insult

    def launch(self):
        self.run(self._token)
