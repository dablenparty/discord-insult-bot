# main.py
import os
import random
import discord

from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
from insultbot import __version__ as __bot_version__, insult_bot, insult_api
from pprint import pprint


def main():
    load_dotenv()
    print("Loaded environment")
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(intents=intents, command_prefix="!")
    print("Instantiated bot")

    _ = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
    bot.load_extension("insultbot.slash_cog")
    print("Loaded slash commands")

    @bot.event
    async def on_ready():
        guilds = bot.guilds
        print(f"\n{bot.user} v{__bot_version__} has loaded in {len(guilds)} guild(s):")
        pprint(guilds)
        print()

    @bot.listen('on_message')
    async def on_message(message: discord.Message):
        message_author = message.author
        if message_author == bot.user:
            return

        # check if it's a DM
        if (is_dm := type(message.channel) is discord.DMChannel) \
                or (insult_bot.bot_was_replied_to(bot, message)
                    or bot.user.id in {member.id for member in message.mentions}
                    or not random.randint(0, 100) % 30):
            insult = insult_bot.generate_insult(message_author) if not is_dm \
                else insult_api.get_insult(who="You", plural=True)
            await message.add_reaction("🖕")  # middle finger emoji
            await message.reply(insult)
            print("Bot replied")

    print("Running bot...")
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
