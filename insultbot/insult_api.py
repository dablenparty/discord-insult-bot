# insult_api.py
"""Wrapper for https://insult.mattbas.org/api/"""
import requests as req

FILE_FORMAT = "txt"
LINK = f"https://insult.mattbas.org/api/insult.{FILE_FORMAT}"


def get_insult(who="%7Buser%7D", plural=False, template: str = None):
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
    response = req.get(LINK, params=params)
    print(f"Received '{response}'")
    return response.content.decode("utf-8").replace("%7Buser%7D", "{user}")  # html handles brackets differently
