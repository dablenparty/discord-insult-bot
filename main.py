# main.py
import random
import discord
from discord_slash import SlashCommand
from dotenv import load_dotenv

from insultbot.insult_bot import InsultBot


def main():
    load_dotenv()
    print("Loaded environment")
    intents = discord.Intents.default()
    intents.members = True
    bot = InsultBot(intents=intents, command_prefix="!")
    print("Instantiated bot")

    _ = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
    bot.load_extension("insultbot.slash_cog")
    print("Loaded slash commands")

    @bot.listen('on_message')
    async def on_message(message: discord.Message):
        message_author = message.author
        if message_author == bot.user:
            return

        # check if it's a DM
        if (is_dm := type(message.channel) is discord.DMChannel) \
                or (bot.talk_back(message)
                    or bot.user.id in {member.id for member in message.mentions}
                    or not random.randint(0, 100) % 30):
            insult = bot.generate_insult(message_author) if not is_dm \
                else bot.insult_api.get_insult(who="You", plural=True)
            bot.recently_insulted = True
            await message.add_reaction("🖕")  # middle finger emoji
            await message.reply(insult)
            print("Bot replied with insult")
        else:
            bot.recently_insulted = False

    bot.launch()


if __name__ == "__main__":
    main()
