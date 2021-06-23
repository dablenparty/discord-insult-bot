# insult_bot.py
import discord
import os
import random

from replit import Database

from . import __version__
from discord.ext import commands


class InsultBot(commands.Bot):
    __slots__ = ["_token", "_database"]

    def __init__(self, **options):
        super().__init__(**options)
        self._token = os.getenv("DISCORD_TOKEN")
        self._database = Database(os.getenv("REPLIT_DB_URL"))

    async def on_ready(self):
        print(f"{self.user} v{__version__} has loaded in the following guilds:")
        for guild in self.guilds:
            print(f" - {guild.name} ({guild.id})\n")

    async def on_guild_remove(self, guild: discord.Guild):
        """
        Removes the guild ID and its data from the database when the bot is removed from said guild

        :param guild: Guild that bot was removed from
        """
        del self._database.get("guilds")[str(guild.id)]

    def add_insult(self, guild: discord.Guild, insult: str, user: discord.User = None):
        db_guilds = self._database.get("guilds")
        # guilds should only be added to the database if the "addinsult" command is invoked to save space
        if str(guild.id) not in db_guilds:
            db_guilds[guild.id] = {"name": guild.name,
                                   "insults": [insult], "customUsers": dict()}
            return
        elif user is None:
            db_guilds.get(str(guild.id)).get("insults").append(insult)
            return
        if str(user.id) not in (custom_users := db_guilds.get(str(guild.id)).get("customUsers")):
            custom_users[user.id] = {
                "name": f"{user.name}#{user.discriminator}", "insults": [insult]}
            return
        custom_users.get("insults").append(insult)

    async def insult(self, guild: discord.Guild, channel: discord.TextChannel, user: discord.User):
        """
        Insults a user

        :param guild: Guild the message originates from
        :param channel: Text channel to send message in
        :param user: User to insult
        """
        if guild is None:
            # this happens when the bot receives a dm. I'll deal with this later
            return
        user_id_string = f"<@{user.id}>"
        insults: list = self._database.get("generic")
        db_guilds: dict = self._database.get("guilds")

        # get guild and user specific insults
        if (guild_data := db_guilds.get(str(guild.id))) is not None:
            insults.extend(guild_data.get("insults"))
            custom_users = guild_data.get("customUsers")
            if str(user.id) in custom_users:
                insults.extend(custom_users.get(str(user.id)).get("insults"))

        chosen_insult = random.choice(insults)
        chosen_insult = chosen_insult.replace("{user}", user_id_string) if "{user}" in chosen_insult \
            else user_id_string + " " + chosen_insult
        await channel.send(chosen_insult)

    def _get_insults_list(self, guild: discord.Guild, user: discord.User) -> list:
        guilds: dict = self._database.get("guilds")
        # making the default return an empty dict allows for chaining even when the key isn't present
        insults = \
            guilds.get(str(guild.id), dict()).get("customUsers", dict()).get(str(user.id), dict()).get("insults", [])\
            if user is not None else guilds.get(str(guild.id), dict()).get("insults", [])
        return insults

    def get_formatted_insult_list(self, guild: discord.Guild, user: discord.User = None):
        lines = []
        insults = self._get_insults_list(guild, user)
        if not len(insults):
            if user is not None:
                return "That dumbass has no custom insults. Add some first next time with the `addinsult` command."
            return "You're not smart enough to have come up with any custom insults for this server yet. " \
                   "Once you pull your head out of your ass, maybe try adding some with the `addinsult` command."

        for i, insult in enumerate(insults, 1):
            lines.append(f"{i}) \"{insult}\"\n")
        # surround the list with backticks to make it stand out
        lines.insert(0, "```apache")
        lines.append("```")
        lines.append(
            "||psst... pro tip, you can use \"{user}\" to tag whoever the bot is insulting||")
        return '\n'.join(lines)

    def remove_insult(self, insult_index: int, guild: discord.Guild, user: discord.User = None):
        if type(insult_index) is not int:
            insult_index = int(insult_index)
        insult_index -= 1  # the printed lists are formatted beginning at 1
        insults = self._get_insults_list(guild, user)
        if not len(insults) or not 0 <= insult_index < len(insults):
            raise IndexError("Index out of bounds")
        del insults[insult_index]

    def launch(self):
        self.run(self._token)
