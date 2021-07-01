# insult_bot.py
import random
import discord

from . import insult_api
from discord.ext import commands
from pprint import pprint


def generate_insult(user: discord.User) -> str:
    """
    Generates and formats an insult from the API

    :param user: User to insult
    :return: Formatted insult
    """
    user_tag = f"<@{user.id}>"  # tags the user
    # 1 in 9 chance to just flip them off
    if not random.randint(1, 9) % 9:
        print("Bot will flip the bird")
        return user_tag + " 🖕"
    insult = insult_api.get_insult()
    insult = insult.replace("{user}", user_tag) if "{user}" in insult \
        else user_tag + " " + insult
    print("Bot generated insult with following data:")
    pprint({"user": {"name": f"{user.name}#{user.discriminator}", "id": user.id}, "insult": insult})
    return insult


def bot_was_replied_to(bot: commands.Bot, message: discord.Message) -> bool:
    """
    Decides if a user is talking back to the bot

    :param bot: Bot whose message was (maybe) replied to
    :param message: Message to analyze
    :return: If the bot was replied to
    """
    if message.reference is not None and message.reference.resolved.author == bot.user:
        print("Bot detected a reply")
        return True
    return False
