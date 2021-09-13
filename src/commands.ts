import { Client, Collection, CommandInteraction } from "discord.js";
import { SlashCommandBuilder } from "@discordjs/builders";
import { readdir } from "fs/promises";
import { join } from "path";
import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v9";

export type SlashCommand = {
  data: SlashCommandBuilder;
  execute(interaction: CommandInteraction): Promise<void>;
};

/**
 * Dynamically reads slash command files into a collection
 *
 * @returns Collection of commands with the command names as keys
 */
export async function readCommandsFromFolder(): Promise<
  Collection<string, SlashCommand>
> {
  const commands = new Collection<string, SlashCommand>();
  try {
    const commandsFolderPath = join(__dirname, "commands");
    const files = await readdir(commandsFolderPath);
    for (const file of files.filter((file) => file.endsWith(".js"))) {
      const command: SlashCommand = require(`${commandsFolderPath}/${file}`);
      commands.set(command.data.name, command);
    }
  } catch (e) {
    console.error(e);
  }
  return commands;
}

/**
 * Registers the slash commands with discord
 *
 * @param commands Commands to register
 * @param client Client to register commands for
 */
export async function registerSlashCommands(
  commands: Collection<string, SlashCommand>,
  client: Client
): Promise<void> {
  const token = process.env.DISCORD_TOKEN || client.token;
  if (!token) throw `Invalid token: '${token}'`;
  const rest = new REST({
    version: "9",
  }).setToken(token);
  const clientId = client.user?.id || process.env.CLIENT_ID;
  const guildId = process.env.GUILD_ID;
  if (!clientId) throw "Cannot retrieve client ID";
  else if (!guildId) throw "Cannot retrieve guild ID";
  const routeCommands =
    process.env.DEV === "1"
      ? Routes.applicationGuildCommands(clientId, guildId)
      : Routes.applicationCommands(clientId);
  await rest.put(routeCommands, {
    body: commands.map((value) => value.data.toJSON()),
  });
}
