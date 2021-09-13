import { generateInsult } from "../insultbot/insultBot";
import { CommandInteraction } from "discord.js";
import { SlashCommandBuilder } from "@discordjs/builders";

export const data = new SlashCommandBuilder()
  .setName("insult")
  .setDescription("Insult someone")
  .addUserOption((option) =>
    option.setName("user").setDescription("User to insult").setRequired(false)
  );

export async function execute(interaction: CommandInteraction) {
  const userToInsult = interaction.options.data.length
    ? interaction.options.data[0].user
    : interaction.user;
  await interaction.reply({ content: await generateInsult(userToInsult) });
}
