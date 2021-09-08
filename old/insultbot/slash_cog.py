# slash_cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, manage_commands
from insultbot import insult_bot


class SlashCog(commands.Cog):
    """
    Derived class for hosting slash commands

    Note: Despite doing away with OOP in the rest of the project, this file will remain in an object-oriented format.
    This allows for less clutter in main.py and a more logical way to read the loading of these commands.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="insult",
                       description="Asks the bot to insult you, or others...",
                       options=[manage_commands.create_option("user",
                                                              "The user you wish to sick the bot on",
                                                              discord.User,
                                                              False)])
    async def _insult_command(self, ctx: SlashContext, user: discord.User = None):
        user_to_insult = ctx.author if user is None else user
        print(f"/insult invoked on {user_to_insult}")
        insult = insult_bot.generate_insult(user_to_insult)
        await ctx.send(content=insult)
        print("/insult succeeded!")

    @cog_ext.cog_slash(name="dap",
                       description="Dap me up")
    async def _dap_me_up_command(self, ctx: SlashContext):
        print(f"/dap invoked on {ctx.author}")
        await ctx.send("👏")
        print("/dap succeeded")


def setup(bot: commands.Bot):
    bot.add_cog(SlashCog(bot))
