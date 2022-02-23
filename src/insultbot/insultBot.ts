import getInsult from "./insultApi";
import { User } from "discord.js";

/**
 * Generates and formats an insult for the bot to send
 *
 * Previous versions of this would tag the user; however, this is no longer necessary as direct message replies are now
 * supported (this was a feature already in the python version, I just never changed the insult formatting)
 *
 * @returns Formatted insult
 */
export async function generateInsult(user?: User): Promise<string> {
  // I felt that replying with the middle finger should tag the user anyways, because of the command. However, I like
  // the thought of the bot not wanting to insult who it wants, and flipping the sender off instead, so it's going to
  // stay that way now and likely won't change again
  if (!(Math.floor(Math.random() * 9) % 9)) return "🖕";
  try {
    if (!user) return await getInsult();
    const insult = await getInsult("{user}", false);
    return insult.replace("{user}", user.toString());
  } catch (e) {
    return "🖕"; // failsafe in case the insult API gets screwed up or goes down
  }
}
