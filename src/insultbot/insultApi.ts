import axios from "axios";

/**
 * Gets an insult from the API found at https://insult.mattbas.org
 *
 * @param who Who to insult
 * @returns Formatted insult
 */
export default async function getInsult(who = "{user}"): Promise<string> {
  const response = await axios.get(
    "https://insult.mattbas.org/api/insult.txt",
    { params: { who } }
  );
  console.log(`Received '${response.status} ${response.statusText}'`);
  return response.data;
}
