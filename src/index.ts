import { config as loadDotenv } from "dotenv";
import { Client, Collection, Guild } from "discord.js";

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

  botClient.once("ready", () => {
    const guilds: Collection<string, Guild> = botClient.guilds.valueOf();
    console.log(
      `${botClient.user?.username} v2.0.0 has loaded in ${guilds.size} guild(s):`
    );
    for (const guild of guilds) console.log(guild.toString());
  });

  try {
    await botClient.login(process.env.DISCORD_TOKEN);
  } catch (e) {
    console.error(e);
    console.error("Shutting down...");
  }
})();
