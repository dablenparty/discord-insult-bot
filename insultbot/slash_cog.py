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
    async def _insult_command(self, ctx: SlashContext, tagged_user: discord.User = None):
        user = ctx.author if tagged_user is None else tagged_user
        await self.bot.insult(ctx.channel, user)


def setup(bot: commands.Bot):
    # InsultBot is a derived class of Bot
    bot.add_cog(SlashCog(bot))
