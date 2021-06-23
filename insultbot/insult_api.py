# insult_api.py
import requests as req


class InsultApi:
    """Wrapper class for https://insult.mattbas.org/api/"""
    __slots__ = ["_file_format", "_link", "_template", "_plural"]

    def __init__(self, file_format="txt", template: str = None, plural=False):
        self._file_format = file_format
        self._template = template
        self._plural = plural
        self._link = f"https://insult.mattbas.org/api/insult.{self._file_format}"

    def get_insult(self):
        params = {"who": "%7Buser%7D"}
        if self._template is not None:
            params["template"] = self._template
        if self._plural:
            params["plural"] = "on"
        response = req.get(self._link, params=params)
        return response.content.decode("utf-8").replace("%7Buser%7D", "{user}")  # html handles brackets differently
