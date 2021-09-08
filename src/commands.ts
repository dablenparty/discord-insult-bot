import { Client, Collection, CommandInteraction } from "discord.js";
import { readdir } from "fs/promises";
import { join } from "path";

export type Command = {
  name: string;
  description: string;
  execute(interaction: CommandInteraction): Promise<void>;
};

/**
 * Dynamically reads slash command files into a collection
 *
 * @returns Collection of commands with the command names as keys
 */
export async function readCommandsFromFolder(): Promise<
  Collection<string, Command>
> {
  const commands = new Collection<string, Command>();
  try {
    const commandsFolderPath = join(__dirname, "commands");
    const files = await readdir(commandsFolderPath);
    for (const file of files.filter((file) => file.endsWith(".js"))) {
      const {
        command,
      }: { command: Command } = require(`${commandsFolderPath}/${file}`);
      commands.set(command.name, command);
    }
  } catch (e) {
    console.error("There was an error reading command files");
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
  commands: Collection<string, Command>,
  client: Client
): Promise<void> {
  for (const [, command] of commands) {
    const app =
      process.env.DEV === "1"
        ? client.guilds.cache.get(process.env.GUILD_ID || "")
        : client.application;
    await app?.commands.create({
      name: command.name,
      description: command.description,
    });
  }
}
