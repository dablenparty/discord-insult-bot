# main.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

from insultbot.insult_bot import InsultBot


def main():
    load_dotenv()
    intents = discord.Intents.default()
    intents.members = True
    cmd_prefix = "/"
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

    @bot.command(name="addinsult")
    async def add_insult(ctx: commands.Context):
        message: discord.Message = ctx.message
        if len(message.mentions) != 1 or message.mention_everyone:
            await ctx.send(f"Usage: `{cmd_prefix}addinsult user insult`")
            return
        user: discord.User = message.mentions[0]
        insult = message.content\
            .replace(f"{cmd_prefix}{ctx.command} ", "")\
            .replace(f"<@!{user.id}> ", "", 1)\
            .replace(f"<@!{user.id}> ", "{user}")
        bot.add_insult_to_user(user, insult)

    bot.launch()


if __name__ == "__main__":
    main()
