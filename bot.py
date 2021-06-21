# bot.py
import random

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path
import json


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_insults", "_custom_users"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        parent_dir = Path(__file__).parent
        self._insults = (parent_dir / "insults.txt").read_text().split('\n')
        with (parent_dir / "custom.json").open() as json_stream:
            self._custom_users: dict = json.load(json_stream).get("users")

    async def on_ready(self):
        print(f"{self.user} has found these users:")
        guild = self.guilds[0]
        members = [str(member.id) + ": " + member.name for member in guild.members]
        print('\n - '.join(members))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if not random.randint(0, 100) % 3:
            await self._insult(message.channel, message.author)

    async def _insult(self, channel: discord.TextChannel, user: discord.User):
        user_id_string = f"<@{user.id}>"
        insult = ""
        if str(user.id) in self._custom_users.keys():
            insult = random.choice(self._custom_users.get(str(user.id), "").get("insults"))
        while not insult.strip():
            insult = random.choice(self._insults)
        insult = insult.replace("{user}", user_id_string) if "{user}" in insult else user_id_string + " " + insult
        await channel.send(insult)

    def launch(self):
        self.run(self._token)


def main() -> None:
    load_dotenv()
    intents = discord.Intents.default()
    intents.members = True
    bot = InsultBot(intents=intents, command_prefix="?")
    bot.launch()


if __name__ == "__main__":
    main()
