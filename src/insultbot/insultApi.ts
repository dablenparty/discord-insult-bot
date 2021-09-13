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
  console.log("Requesting insult from API...");
  const response = await axios.get(
    "https://insult.mattbas.org/api/insult.txt",
    { params: plural ? { who, plural } : { who } }
  );
  console.log(`Received '${response.status} ${response.statusText}'`);
  return response.data;
}
