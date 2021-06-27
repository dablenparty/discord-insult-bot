# slash_cog.py

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from .insult_bot import InsultBot


class SlashCog(commands.Cog):
    def __init__(self, bot: InsultBot):
        self.bot: InsultBot = bot

    @cog_ext.cog_slash(name="insult")
    async def _insult_command(self, ctx: SlashContext):
        await self.bot.insult(ctx.channel, ctx.author)


def setup(bot: commands.Bot):
    # InsultBot is a derived class of Bot
    bot.add_cog(SlashCog(bot))
