import { User } from "discord.js";
import getInsult from "./insultApi";

/**
 * Generates and formats an insult for the bot to send
 *
 * @param user User to insult
 * @returns Formatted insult
 */
export async function generateInsult(user: User): Promise<string> {
  if (!(Math.floor(Math.random() * 9) % 9)) return "🖕";
  try {
    return (await getInsult()).replace("{user}", user.toString());
  } catch (e) {
    return "🖕"; // failsafe in case the insult API gets screwed up or goes down
  }
}
