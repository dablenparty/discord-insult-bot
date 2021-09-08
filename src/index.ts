import { config as loadDotenv } from "dotenv";
import { Client, Collection, Guild, User } from "discord.js";
import { generateInsult } from "./insultbot/insultBot";

(async () => {
  loadDotenv();
  const botClient = new Client({
    intents: [
      "GUILD_MEMBERS",
      "GUILD_MESSAGE_REACTIONS",
      "GUILD_MESSAGES",
      "GUILDS",
    ],
  });

  const handEmojis = ["✋", "🤚", "🖐️"];

  botClient.once("ready", () => {
    const guilds: Collection<string, Guild> = botClient.guilds.valueOf();
    console.log(
      `${botClient.user?.username} v2.0.0 has loaded in ${guilds.size} guild(s):`
    );
    for (const guild of guilds) console.log(guild.toString());
  });

  botClient.on("messageCreate", async (message) => {
    if (message.author.equals(botClient.user as User)) return;
    const botId: string | undefined = botClient.user?.id;
    const botMentioned: boolean = botId
      ? message.mentions.users.has(botId)
      : false;
    const botRepliedTo: boolean = message.reference?.messageId
      ? (
          await message.channel.messages.fetch(message.reference?.messageId)
        ).author.equals(botClient.user as User)
      : false;
    if (
      message.channel.type === "DM" ||
      botMentioned ||
      botRepliedTo ||
      !(Math.floor(Math.random() * 100) % 50)
    ) {
      if (
        botMentioned &&
        handEmojis.some((emoji) => message.content.includes(emoji))
      ) {
        await message.reply({ content: "👏" });
      } else {
        const insult: string = await generateInsult(message.author);
        await message.react("🖕");
        await message.reply({ content: insult });
      }
    }
  });

  try {
    await botClient.login(process.env.DISCORD_TOKEN);
  } catch (e) {
    console.error(e);
    console.error("Shutting down...");
  }
})();
