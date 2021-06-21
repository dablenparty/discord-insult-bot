# bot.py
import random

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


class InsultBot(commands.Bot):
    __slots__ = ["_token"]
    _insults = ["you're a sad excuse for a human being",
                "the fact that your mother missed with the coat hanger is proof to me that God doesn't exist",
                "maybe if you could stomach to look in the mirror more often you might realize why you don't look in the mirror"]

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

        if not random.randint(0, 100) % 3:
            await self._insult(message.channel, message.author)

    async def _insult(self, channel: discord.TextChannel, user: discord.User):
        await channel.send(f"<@{user.id}> {random.choice(self._insults)}")

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
