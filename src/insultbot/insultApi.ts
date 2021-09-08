import axios from "axios";

/**
 * Gets an insult from the API found at https://insult.mattbas.org
 *
 * @param who Who to insult
 * @param plural Whether to insult multiple people or not
 * @returns Formatted insult
 */
export default async function getInsult(
  who = "You",
  plural = true
): Promise<string> {
  const response = await axios.get(
    "https://insult.mattbas.org/api/insult.txt",
    { params: { who, plural } }
  );
  console.log(`Received '${response.status} ${response.statusText}'`);
  return response.data;
}
