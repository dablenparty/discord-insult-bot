# bot.py
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

from insultbot.insult_bot import InsultBot

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
