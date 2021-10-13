import { config as loadDotenv } from "dotenv";
import { Client, Collection, Guild, User } from "discord.js";
import { generateInsult } from "./insultbot/insultBot";
import {
  SlashCommand,
  readCommandsFromFolder,
  registerSlashCommands,
} from "./commands";

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

  let commands: Collection<string, SlashCommand>;

  botClient.once("ready", async () => {
    const guilds: Collection<string, Guild> = botClient.guilds.valueOf();
    console.log(
      `${botClient.user?.username} v2.0.0 has loaded in ${guilds.size} guild(s):`
    );
    for (const guild of guilds) console.log(guild.toString());

    try {
      commands = await readCommandsFromFolder();
      await registerSlashCommands(commands, botClient);
    } catch (e) {
      console.error(e);
      console.error("There was an error registering slash commands");
    }
  });

  botClient.on("interactionCreate", async (interaction) => {
    if (!interaction.isCommand()) return;
    const command = commands.get(interaction.commandName);
    if (!command) return;
    try {
      await command.execute(interaction);
    } catch (e) {
      console.error(e);
      await interaction.reply({
        content: "There was an issue running this command",
      });
    }
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
      !(Math.floor(Math.random() * 100) % 40)
    ) {
      if (
        botMentioned &&
        handEmojis.some((emoji) => message.content.includes(emoji))
      ) {
        await message.reply({ content: "👏" });
      } else {
        const insult: string = await generateInsult();
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
