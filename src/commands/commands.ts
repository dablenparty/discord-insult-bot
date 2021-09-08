import { Client, Collection, CommandInteraction } from "discord.js";

export type Command = {
  name: string;
  description: string;
  execute(interaction: CommandInteraction): Promise<void>;
};

export async function registerSlashCommands(
  commands: Collection<string, Command>,
  client: Client
) {
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
