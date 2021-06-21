import discord
import json
import os
import random
from . import __version__
from discord.ext import commands
from pathlib import Path


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_insults", "_custom_users"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        parent_dir = Path(__file__).parent
        with (parent_dir / "insults.json").open() as json_stream:
            data: dict = json.load(json_stream)
            self._insults = data.get("generic")
            self._custom_users: dict = data.get("users")

    async def on_ready(self):
        print(f"{self.user} v{__version__} has loaded in the following guilds:")
        for guild in self.guilds:
            print(f" - {guild.name} ({guild.id})\n")

    async def insult(self, channel: discord.TextChannel, user: discord.User):
        """
        Insults a user

        :param channel: Text channel to send message in
        :param user: User to insult
        """
        user_id_string = f"<@{user.id}>"
        chosen_insult = ""

        insults = self._insults
        if str(user.id) in self._custom_users.keys():
            insults.extend(self._custom_users.get(str(user.id), "").get("insults"))

        while not chosen_insult.strip():
            chosen_insult = random.choice(self._insults)
        chosen_insult = chosen_insult.replace("{user}", user_id_string) if "{user}" in chosen_insult else user_id_string + " " + chosen_insult
        await channel.send(chosen_insult)

    def launch(self):
        self.run(self._token)
