from asyncio import run
from collections import deque
from csv import reader, writer
from os import makedirs
from os.path import join
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping

from ijson import kvitems
from loguru import logger
from orjson import OPT_INDENT_2, dumps, loads

ROOT = "G:\\Assets_Dev"
DATA = join(ROOT, "Data")
FLATTENED = join(DATA, "Flattened")
SEMI_FLATTENED = join(DATA, "SemiFlattened")
PARQUET = join(DATA, "Parquet")
RAW = join(DATA, "Raw")
CSV = join(DATA, "Csv")


def __flatten(data: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}

    stack = deque([("", data)])

    while stack:
        path, value = stack.popleft()

        if isinstance(value, Mapping):
            for key, child in value.items():
                child_path = key if not path else f"{path}.{key}"
                stack.append((child_path, child))

        elif isinstance(value, list):
            for i, child in enumerate(value):
                child_path = f"{path}[{i}]"
                stack.append((child_path, child))

        else:
            result[path] = value

    return result


def flatten_dict(filepath: str | Path, output_path: str | Path) -> None:
    all_times = []
    result: dict[str, Any] = {}
    with open(filepath, "rb") as f, open(output_path, "wb") as o:
        for k, v in kvitems(f, ""):
            start_flattening = perf_counter()
            result.update(__flatten(v))
            end_flattening = perf_counter()
            all_times.append(end_flattening - start_flattening)
        logger.info("Flattened Dict at {} {:.2f}s", filepath, sum(all_times))
        o.write(dumps(result))


def get_keys() -> list[str]:
    names = []
    with open(join(ROOT, "table_names.csv"), "r", encoding="UTF-8") as f:
        csv_reader = reader(f, delimiter=",")
        for item in csv_reader:
            if item[0] == "id":
                continue
            names.append(item[1])
    return names


def create_directories():
    makedirs(FLATTENED, exist_ok=True)
    makedirs(SEMI_FLATTENED, exist_ok=True)
    makedirs(PARQUET, exist_ok=True)
    makedirs(RAW, exist_ok=True)
    makedirs(CSV, exist_ok=True)


def create_inventory_csv():
    w_total: int = 0
    a_total: int = 0
    s_total: int = 0

    weapons_path: str = join(DATA, "weapons.csv")
    armor_path: str = join(DATA, "armor.csv")
    sockets_path: str = join(DATA, "sockets.csv")

    with (
        open(join(RAW, "DestinyInventoryItemDefinition.json"), "rb") as rf,
        open(weapons_path, "w", encoding="UTF-8") as weapon_desc,
        open(armor_path, "w", encoding="UTF-8") as armor_desc,
        open(sockets_path, "w", encoding="UTF-8") as sockets_desc,
    ):
        weapons_csv_writer = writer(
            weapon_desc, delimiter=",", lineterminator="\n", doublequote=True
        )
        armor_csv_writer = writer(
            armor_desc, delimiter=",", lineterminator="\n", doublequote=True
        )
        sockets_csv_writer = writer(
            sockets_desc, delimiter=",", lineterminator="\n", doublequote=True
        )

        weapons_csv_writer.writerow(["id", "json"])
        armor_csv_writer.writerow(["id", "json"])
        sockets_csv_writer.writerow(["id", "json"])

        start_time = perf_counter()
        for k, v in kvitems(rf, ""):
            item_type = v["itemType"]

            match item_type:
                case 3:
                    weapons_csv_writer.writerow([k, dumps(v).decode("UTF-8")])
                    w_total += 1
                case 2:
                    armor_csv_writer.writerow([k, dumps(v).decode("UTF-8")])
                    a_total += 1
                case 19:
                    sockets_csv_writer.writerow([k, dumps(v).decode("UTF-8")])
                    s_total += 1

        end_time = perf_counter()
        logger.info("Wrote {} rows to weapons.csv", w_total)
        logger.info("Wrote {} rows to armor.csv", a_total)
        logger.info("Wrote {} rows to sockets.csv", s_total)
        logger.info("Total Time {:.2f}s", end_time - start_time)


def process_weapon(old_data: dict):
    return {
        "name": old_data.get("displayProperties", {}).get("name"),
        "icon": old_data.get("displayProperties", {}).get("icon"),
        "iconWatermark": old_data.get("iconWatermark"),
    }


async def main():
    # create_directories()
    # create_inventory_csv()
    with (
        open(join(DATA, "weapons.csv"), "r", encoding="UTF-8") as f,
        open(join(DATA, "weapons.jsonl"), "w", encoding="UTF-8") as w,
    ):
        weapon_reader = reader(f, delimiter=",", doublequote=True)
        for k, v in weapon_reader:
            if k == "id":
                continue
            weapon_json = loads(v)
            w.write(dumps(process_weapon(weapon_json)).decode("UTF-8") + "\n")


if __name__ == "__main__":
    run(main())
