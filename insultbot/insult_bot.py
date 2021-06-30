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

    # def add_insult(self, guild: discord.Guild, insult: str, user: discord.User = None):
    #     db_guilds = self._database.get("guilds")
    #     # guilds should only be added to the database if the "addinsult" command is invoked to save space
    #     if str(guild.id) not in db_guilds:
    #         db_guilds[guild.id] = {"name": guild.name,
    #                                "insults": [insult], "customUsers": dict()}
    #         return
    #     elif user is None:
    #         db_guilds.get(str(guild.id)).get("insults").append(insult)
    #         return
    #     if str(user.id) not in (custom_users := db_guilds.get(str(guild.id)).get("customUsers")):
    #         custom_users[user.id] = {
    #             "name": f"{user.name}#{user.discriminator}", "insults": [insult]}
    #         return
    #     custom_users.get("insults").append(insult)

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

    # def _get_insults_list(self, guild: discord.Guild, user: discord.User) -> list:
    #     guilds: dict = self._database.get("guilds")
    #     # making the default return an empty dict allows for chaining even when the key isn't present
    #     insults = \
    #         guilds.get(str(guild.id), dict()).get("customUsers", dict()).get(str(user.id), dict()).get("insults", [])\
    #         if user is not None else guilds.get(str(guild.id), dict()).get("insults", [])
    #     return insults

    # def get_formatted_insult_list(self, guild: discord.Guild, user: discord.User = None):
    #     lines = []
    #     insults = self._get_insults_list(guild, user)
    #     if not len(insults):
    #         if user is not None:
    #             return "That dumbass has no custom insults. Add some first next time with the `addinsult` command."
    #         return "You're not smart enough to have come up with any custom insults for this server yet. " \
    #                "Once you pull your head out of your ass, maybe try adding some with the `addinsult` command."
    #
    #     for i, insult in enumerate(insults, 1):
    #         lines.append(f"{i}) \"{insult}\"\n")
    #     # surround the list with backticks to make it stand out
    #     lines.insert(0, "```apache")
    #     lines.append("```")
    #     lines.append(
    #         "||psst... pro tip, you can use \"{user}\" to tag whoever the bot is insulting||")
    #     return '\n'.join(lines)

    # def remove_insult(self, insult_index: int, guild: discord.Guild, user: discord.User = None):
    #     if type(insult_index) is not int:
    #         insult_index = int(insult_index)
    #     insult_index -= 1  # the printed lists are formatted beginning at 1
    #     insults = self._get_insults_list(guild, user)
    #     if not len(insults) or not 0 <= insult_index < len(insults):
    #         raise IndexError("Index out of bounds")
    #     del insults[insult_index]

    def launch(self):
        self.run(self._token)
