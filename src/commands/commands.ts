import { CommandInteraction } from "discord.js";

export type Command = {
  name: string;
  description: string;
  execute(interaction: CommandInteraction): Promise<void>;
};
