import axios from "axios";

export default async function getInsult(who = "{user}") {
  const response = await axios.get(
    "https://insult.mattbas.org/api/insult.txt",
    { params: { who } }
  );
  console.log(`Received '${response.status} ${response.statusText}'`);
  return response.data;
}
