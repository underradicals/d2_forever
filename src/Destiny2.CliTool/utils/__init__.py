from typing import Any, Mapping

from orjson import OPT_INDENT_2, dumps, loads

from common import MANIFEST_FILE
from enums import Language


def __topLevelContentPaths(language: Language, top_level_name: str):
    with open(MANIFEST_FILE, "rb") as rf:
        data: dict = loads(rf.read())

        if language is None:
            print(
                dumps(
                    data["Response"][top_level_name],
                    option=OPT_INDENT_2,
                ).decode("UTF-8")
            )
        else:
            print(
                dumps(
                    data["Response"][top_level_name][language.value],
                    option=OPT_INDENT_2,
                ).decode("UTF-8")
            )


def get_json_value(data: Mapping[str, Any], path: str):
    """
    Safely extract a value from a nested JSON/dict object using dot notation.

    Example:
        path = "Response.jsonWorldComponentContentPaths.en.DestinyInventoryItemDefinition"
    """

    current = data

    for key in path.split("."):
        if not isinstance(current, dict):
            return None

        current = current.get(key)

        if current is None:
            return None

    return current
