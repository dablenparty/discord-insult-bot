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
        with (parent_dir / "insults.json").open() as json_stream:
            data: dict = json.load(json_stream)
            self._insults = data.get("generic")
            self._custom_users: dict = data.get("users")

    async def on_ready(self):
        print(f"{self.user} has found these users:")
        guild = self.guilds[0]
        members = [str(member.id) + ": " + member.name for member in guild.members]
        print('\n - '.join(members))

    async def insult(self, channel: discord.TextChannel, user: discord.User):
        user_id_string = f"<@{user.id}>"
        insults = self._insults
        chosen_insult = ""
        if str(user.id) in self._custom_users.keys():
            insults.extend(self._custom_users.get(str(user.id), "").get("insults"))
        while not chosen_insult.strip():
            chosen_insult = random.choice(self._insults)
        chosen_insult = chosen_insult.replace("{user}", user_id_string) if "{user}" in chosen_insult else user_id_string + " " + chosen_insult
        await channel.send(chosen_insult)

    def launch(self):
        self.run(self._token)


if __name__ == "__main__":
    load_dotenv()
    intents = discord.Intents.default()
    intents.members = True
    cmd_prefix = "?"
    bot = InsultBot(intents=intents, command_prefix=cmd_prefix)

    @bot.listen('on_message')
    async def on_message(message: discord.Message, command=False):
        if message.author == bot.user or (not command and message.content.startswith(cmd_prefix)):
            return

        if command or not random.randint(0, 100) % 15:
            await bot.insult(message.channel, message.author)

    @bot.command(name="insult")
    async def insult_command(ctx: commands.Context):
        await on_message(ctx.message, True)

    bot.launch()
