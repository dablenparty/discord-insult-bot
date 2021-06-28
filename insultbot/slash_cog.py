# slash_cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, manage_commands
from .insult_bot import InsultBot


class SlashCog(commands.Cog):
    def __init__(self, bot: InsultBot):
        self.bot: InsultBot = bot

    @cog_ext.cog_slash(name="insult",
                       description="Asks the bot to insult you, or others...",
                       options=[manage_commands.create_option("user",
                                                              "The user you wish to sick the bot on",
                                                              discord.User,
                                                              False)])
    async def _insult_command(self, ctx: SlashContext, user: discord.User = None):
        user_to_insult = ctx.author if user is None else user
        insult = self.bot.generate_insult(user_to_insult)
        await ctx.send(content=insult)


def setup(bot: InsultBot):
    # InsultBot is a derived class of Bot, so this is OK
    bot.add_cog(SlashCog(bot))
