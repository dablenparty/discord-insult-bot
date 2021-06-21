import discord
import json
import os
import random
from . import __version__
from discord.ext import commands
from pathlib import Path


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_insult_json_data", "_insults_file", "_last_file_mtime"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        self._insults_file = Path(__file__).parent / "insults.json"
        self._load_insults()

    def _load_insults(self):
        with self._insults_file.open() as json_stream:
            self._insult_json_data: dict = json.load(json_stream)
        self._last_file_mtime = os.path.getmtime(self._insults_file)

    async def on_ready(self):
        print(f"{self.user} v{__version__} has loaded in the following guilds:")
        for guild in self.guilds:
            print(f" - {guild.name} ({guild.id})\n")

    def _check_mtime(self):
        if os.path.getmtime(self._insults_file) != self._last_file_mtime:
            self._load_insults()

    def _try_add_user_to_list(self, user: discord.User, custom_users: dict):
        if str(user.id) in custom_users:
            return False
        custom_users[user.id] = \
            {"name": f"{user.name}#{user.discriminator}", "insults": []}
        with self._insults_file.open(mode='w') as json_file:
            json.dump(self._insult_json_data, json_file)
        return True

    async def insult(self, channel: discord.TextChannel, user: discord.User):
        """
        Insults a user

        :param channel: Text channel to send message in
        :param user: User to insult
        """
        self._check_mtime()  # on every message, check if new insults need to be loaded or not

        user_id_string = f"<@{user.id}>"
        chosen_insult = ""
        insults: list = self._insult_json_data.get("generic")
        custom_users: dict = self._insult_json_data.get("customUsers")

        if not self._try_add_user_to_list(user, custom_users):
            insults.extend(custom_users.get(str(user.id), "").get("insults"))

        while not chosen_insult.strip():
            chosen_insult = random.choice(insults)
        chosen_insult = chosen_insult.replace("{user}", user_id_string) if "{user}" in chosen_insult \
            else user_id_string + " " + chosen_insult
        await channel.send(chosen_insult)

    def launch(self):
        self.run(self._token)
