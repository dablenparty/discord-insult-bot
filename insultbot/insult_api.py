# insult_api.py
import requests as req


class InsultApi:
    """Wrapper class for https://insult.mattbas.org/api/"""
    __slots__ = ["_file_format", "_link"]

    def __init__(self, file_format="txt"):
        self._file_format = file_format
        self._link = f"https://insult.mattbas.org/api/insult.{self._file_format}"

    def get_insult(self, who="%7Buser%7D", plural=False, template: str = None):
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
        response = req.get(self._link, params=params)
        print(f"Received '{response}'")
        return response.content.decode("utf-8").replace("%7Buser%7D", "{user}")  # html handles brackets differently
