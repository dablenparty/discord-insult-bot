# insult_bot.py
import discord
import os
import random

from replit import Database

from . import __version__
from discord.ext import commands


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_database"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        self._database = Database(os.getenv("REPLIT_DB_URL"))

    async def on_ready(self):
        print(f"{self.user} v{__version__} has loaded in the following guilds:")
        for guild in self.guilds:
            print(f" - {guild.name} ({guild.id})\n")

    def _try_add_user_to_list(self, user: discord.User):
        known_users = self._database.get("knownUsers")
        if str(user.id) in known_users:
            return False
        known_users[user.id] = \
            {"name": f"{user.name}#{user.discriminator}", "insults": []}
        return True

    def add_insult_to_user(self, user: discord.User, insult: str):
        known_users: dict = self._insult_json_data.get("knownUsers")
        self._try_add_user_to_list(user)
        known_users.get(str(user.id)).get("insults").append(insult)

    async def insult(self, channel: discord.TextChannel, user: discord.User):
        """
        Insults a user

        :param channel: Text channel to send message in
        :param user: User to insult
        """
        user_id_string = f"<@{user.id}>"
        insults: list = self._database.get("generic")
        known_users: dict = self._database.get("knownUsers")

        if not self._try_add_user_to_list(user):
            insults.extend(known_users.get(str(user.id), "").get("insults"))

        chosen_insult = random.choice(insults)
        chosen_insult = chosen_insult.replace("{user}", user_id_string) if "{user}" in chosen_insult \
            else user_id_string + " " + chosen_insult
        await channel.send(chosen_insult)

    def launch(self):
        self.run(self._token)
