import { Command } from "../commands";
import { generateInsult } from "../insultbot/insultBot";

export const command: Command = {
  description: "Insult someone",
  name: "insult",
  async execute(interaction) {
    await interaction.reply({ content: await generateInsult() });
  },
};
