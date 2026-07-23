from os.path import join

import typer
from ijson import kvitems
from orjson import OPT_INDENT_2, dumps, loads

from common import MANIFEST_FILE, RAW
from enums import DestinyTables, Language
from utils import __topLevelContentPaths, get_json_value

app = typer.Typer()


LANGUAGE_OPT = typer.Option(
    None,
    "--language",
    "-l",
    help="Language Codes: (e.g. en, fr, de, es, es-mx, it, ja, pt-br, ru, pl, ko, zh-cht, zh-chs)",
)

TABLE_NAME_OPT = typer.Option(
    None, "--tableName", "-t", help="The name of the table you want retrieved"
)

TABLE_ID_OPT = typer.Option(
    None,
    "--id",
    "-i",
)

TABLE_ITEM_NAME_OPT = typer.Option(
    None,
    "--name",
    "-n",
)

TABLE_TOP_LEVEL_KEY_OPT = typer.Option(
    None,
    "--key",
    "-k",
)


@app.command()
def manifest():
    with open(MANIFEST_FILE, "rb") as rf:
        data: dict = loads(rf.read())
        print(dumps(data, option=OPT_INDENT_2).decode("UTF-8"))


@app.command()
def mwcp(language: Language = LANGUAGE_OPT):
    __topLevelContentPaths(language, "mobileWorldContentPaths")


@app.command("mobileWorldContentPaths")
def mobileWorldContentPaths(language: Language = LANGUAGE_OPT):
    __topLevelContentPaths(language, "mobileWorldContentPaths")


@app.command()
def jwcp(language: Language = LANGUAGE_OPT):
    __topLevelContentPaths(language, "jsonWorldContentPaths")


@app.command("jsonWorldContentPaths")
def jsonWorldContentPaths(language: Language = LANGUAGE_OPT):
    __topLevelContentPaths(language, "jsonWorldContentPaths")


@app.command()
def version():
    with open(MANIFEST_FILE, "rb") as rf:
        data: dict = loads(rf.read())
        print(data["Response"]["version"])


@app.command()
def table(
    table_name: DestinyTables = TABLE_NAME_OPT,
    id: int | None = TABLE_ID_OPT,
    weapon_name: str | None = TABLE_ITEM_NAME_OPT,
    top_level_key: str | None = TABLE_TOP_LEVEL_KEY_OPT,
):
    filename = join(RAW, f"{table_name.value}.json")

    if id is not None:
        with open(filename, "rb") as rf:
            data = loads(rf.read())
            obj = data.get(str(id))

        if obj is None:
            raise typer.BadParameter(f"{id} not found")
        if top_level_key is not None:
            result = get_json_value(obj, top_level_key)
            print(dumps(result, option=OPT_INDENT_2).decode())
            return
        print(dumps(obj, option=OPT_INDENT_2).decode())

    elif weapon_name is not None:
        with open(filename, "rb") as rf:
            for _, value in kvitems(rf, ""):
                if value.get("displayProperties", {}).get("name") == weapon_name:
                    if top_level_key is not None:
                        result = get_json_value(value, top_level_key)
                        print(dumps(result, option=OPT_INDENT_2).decode())
                        return
                    print(dumps(value, option=OPT_INDENT_2).decode())

        raise typer.BadParameter(f"{weapon_name} not found")

    else:
        raise typer.BadParameter("Specify either --id or --name.")


if __name__ == "__main__":
    app()

# python main.py show --tableName DestinyInventoryItemDefinition --id 12345657
