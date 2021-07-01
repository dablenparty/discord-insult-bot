# insult_api.py
import requests as req


class InsultApi:
    """Wrapper class for https://insult.mattbas.org/api/"""
    file_format = "txt"
    __link = f"https://insult.mattbas.org/api/insult.{file_format}"

    @classmethod
    def get_insult(cls, who="%7Buser%7D", plural=False, template: str = None):
        """
        Requests an insult from the API

        :param who: Who to insult
        :param plural: Whether or not to insult multiple people
        :param template: Template to follow (recommend leaving this as None)
        :return: Formatted insult
        """
        params = {"who": who}
        if template is not None:
            params["template"] = template
        if plural:
            params["plural"] = "on"
        print("Requesting insult from API...")
        response = req.get(cls.__link, params=params)
        print(f"Received '{response}'")
        return response.content.decode("utf-8").replace("%7Buser%7D", "{user}")  # html handles brackets differently
