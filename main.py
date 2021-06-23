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

        # message.guild will be None if its a DM
        if message.guild is not None and (command or not random.randint(0, 100) % 30):
            await bot.insult(message.guild, message.channel, message.author)

    @bot.command(name="insult")
    async def insult_command(ctx: commands.Context):
        await on_message(ctx.message, True)

    @bot.command(name="addinsult")
    async def add_insult(ctx: commands.Context):
        message: discord.Message = ctx.message
        insult = message.content.replace(f"{cmd_prefix}{ctx.command} ", "")
        mentions = message.mentions
        user = None if not len(mentions) else mentions[0]  # uses the first mention in the message
        if user is not None:
            insult = insult.replace(f"<@!{user.id}> ", "", 1).replace(f"<@!{user.id}>", "{user}")
        bot.add_insult(ctx.guild, insult, user)
        await message.add_reaction("👌")

    @bot.command(name="listinsults")
    async def list_insults(ctx: commands.Context):
        mentions: list = ctx.message.mentions
        user = None if not len(mentions) else mentions[0]  # uses the first mention in the message
        formatted_string = bot.get_formatted_insult_list(ctx.guild, user)
        await ctx.send(formatted_string)

    @bot.command(name="removeinsult")
    async def remove_insult(ctx: commands.Context):
        message: discord.Message = ctx.message
        mentions: list = message.mentions
        user = None if not len(mentions) else mentions[0]  # uses the first mention in the message
        insult_index = message.content.split(" ")[-1]
        try:
            bot.remove_insult(insult_index, ctx.guild, user)
            await message.add_reaction("👌")
        except (IndexError, ValueError):
            await ctx.send(f"Can't remove what isn't there. Make sure that `{insult_index}` is at least a number, "
                           "then make sure it actually exists. The fact I have to tell you this...")

    bot.launch()


if __name__ == "__main__":
    main()
