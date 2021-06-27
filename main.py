# main.py
import os
import random
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from insultbot.insult_bot import InsultBot


def main():
    load_dotenv()
    intents = discord.Intents.default()
    intents.members = True
    bot = InsultBot(intents=intents, command_prefix="!")

    # load the slash commands
    _ = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
    bot.load_extension("insultbot.slash_cog")

    @bot.listen('on_message')
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return

        # message.guild will be None if its a DM
        if message.guild is not None and (bot.user.id in {member.id for member in message.mentions} or not random.randint(0, 100) % 30):
            await bot.insult(message.channel, message.author, message)

    bot.launch()


if __name__ == "__main__":
    main()
