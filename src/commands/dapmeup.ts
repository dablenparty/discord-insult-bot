import { CommandInteraction } from "discord.js";
import { SlashCommandBuilder } from "@discordjs/builders";

export const data = new SlashCommandBuilder()
  .setName("dapmeup")
  .setDescription("Dap up the bot");

export async function execute(interaction: CommandInteraction) {
  await interaction.reply({ content: "👏" });
}
