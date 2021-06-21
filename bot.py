# bot.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


class InsultBot(commands.Bot):
    __slots__ = ["_token"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")

    async def on_ready(self):
        print(f"{self.user} has found these users:")
        guild = self.guilds[0]
        members = [member.name for member in guild.members]
        print('\n - '.join(members))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        response = f"<@{message.author.id}> idiot"
        await message.channel.send(response)

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
