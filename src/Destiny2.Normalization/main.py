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


def create_csv_for_weapon_armor_sockets():
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
        weapons_csv_writer = writer(weapon_desc, delimiter=",", lineterminator="\n", doublequote=True)
        armor_csv_writer = writer(armor_desc, delimiter=",", lineterminator="\n", doublequote=True)
        sockets_csv_writer = writer(sockets_desc, delimiter=",", lineterminator="\n", doublequote=True)

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


def create_csv_for_stats_plugsets_damagetypes():
    s_total: int = 0
    p_total: int = 0
    d_total: int = 0

    stats_path: str = join(DATA, "stats.csv")
    plug_set_path: str = join(DATA, "plug_set.csv")
    damage_type_path: str = join(DATA, "damage_type.csv")

    with (
        open(join(RAW, "DestinyStatDefinition.json"), "rb") as stat_f,
        open(join(RAW, "DestinyPlugSetDefinition.json"), "rb") as plug_f,
        open(join(RAW, "DestinyDamageTypeDefinition.json"), "rb") as damage_f,
        open(stats_path, "w", encoding="UTF-8") as stats_path_desc,
        open(plug_set_path, "w", encoding="UTF-8") as plug_set_path_desc,
        open(damage_type_path, "w", encoding="UTF-8") as damage_type_path_desc,
    ):
        stats_path_writer = writer(stats_path_desc, delimiter=",", lineterminator="\n", doublequote=True)
        plug_set_path_writer = writer(plug_set_path_desc, delimiter=",", lineterminator="\n", doublequote=True)
        damage_type_path_writer = writer(damage_type_path_desc, delimiter=",", lineterminator="\n", doublequote=True)

        stats_path_writer.writerow(["id", "json"])
        plug_set_path_writer.writerow(["id", "json"])
        damage_type_path_writer.writerow(["id", "json"])

        start_time = perf_counter()
        for index, desc in enumerate([stat_f, plug_f, damage_f]):
            for k, v in kvitems(desc, "", use_float=True):
                if index == 0:
                    stats_path_writer.writerow([k, dumps(v).decode("UTF-8")])
                    s_total += 1

                if index == 1:
                    plug_set_path_writer.writerow([k, dumps(v).decode("UTF-8")])
                    p_total += 1

                if index == 2:
                    damage_type_path_writer.writerow([k, dumps(v).decode("UTF-8")])
                    d_total += 1

        end_time = perf_counter()
        logger.info("Wrote {} rows to stats.csv", s_total)
        logger.info("Wrote {} rows to plug_sets.csv", p_total)
        logger.info("Wrote {} rows to damage_types.csv", d_total)
        logger.info("Total Time {:.2f}s", end_time - start_time)


def process_investment_stats(v, item_dict, stats_dict):
    stats_object: list = v["investmentStats"]
    if len(stats_object) != 0:
        item_dict["stats"] = []
        for item in stats_object:
            hash = str(item["statTypeHash"])
            if hash == "1480404414" or hash == "1935470627" or hash == "1885944937" or hash == "3209419233":
                continue
            else:
                value = item["value"]
                item_dict["stats"].append(
                    {
                        "name": stats_dict[hash]["displayProperties"]["name"],
                        "value": value,
                        "description": stats_dict[hash]["displayProperties"]["description"],
                    }
                )
    else:
        item_dict["stats"] = []


def extract_socket_objects(plug_set_dict, weapon_perk, key):
    return [x["plugItemHash"] for x in plug_set_dict[str(weapon_perk[key])]["reusablePlugItems"]]


def extract_inventory_item_definition(hash, inventory_dict, stats_dict):
    item_dict = {}
    inventory_object = inventory_dict[hash]
    object_type = inventory_object["itemTypeDisplayName"]
    return_value = {
        "type": object_type,
        "name": inventory_object["displayProperties"]["name"],
        "description": inventory_object["displayProperties"]["description"],
        "icon": inventory_object["displayProperties"]["icon"],
        "stats": item_dict,
    }
    process_investment_stats(inventory_object, return_value, stats_dict)
    return object_type, return_value


def process_equipping_block(item_dict, v):
    item_dict["slot"] = {}
    ammoId = v["equippingBlock"]["ammoType"]
    slotTypeId = v["equippingBlock"]["equipmentSlotTypeHash"]

    match slotTypeId:
        case 1498876634:
            item_dict["slot"]["type"] = "Kinetic Weapons"
            item_dict["slot"]["description"] = "Weapons that deal kinetic damage. Most effective when dealing with unshielded enemies."
        case 2465295065:
            item_dict["slot"]["type"] = "Energy Weapons"
            item_dict["slot"]["description"] = "Weapons that deal Arc, Solar, or Void damage. Most effective when dealing with shielded enemies."
        case 953998645:
            item_dict["slot"]["type"] = "Power Weapons"
            item_dict["slot"]["description"] = "Machine guns and rocket launchers."

    match ammoId:
        case 1:
            item_dict["slot"]["ammo_type"] = "Primary"
        case 2:
            item_dict["slot"]["ammo_type"] = "Special"
        case 3:
            item_dict["slot"]["ammo_type"] = "Heavy"


def process_sockets(v, item_dict, plug_set_dict, inventory_dict, stats_dict):
    socket_categories = v["sockets"]["socketCategories"]
    socket_entries = v["sockets"]["socketEntries"]

    if socket_categories is None:
        raise TypeError("Socket Categories cannot be None")

    if socket_entries is None:
        raise TypeError("Socket Entries cannot be None")

    item_dict["perks"] = {}
    item_dict["perks"]["WeaponPerks"] = {}

    for socket_category in socket_categories:
        socket_category_hash = socket_category["socketCategoryHash"]

        if socket_category_hash == 3956125808:  # INTRINSIC TRAITS
            socket_indexes = socket_category["socketIndexes"]

            for index in socket_indexes:
                intrinsic_socket = socket_entries[index]
                single_initial_hash = str(intrinsic_socket["singleInitialItemHash"])
                t, inventory_socket_object = extract_inventory_item_definition(single_initial_hash, inventory_dict, stats_dict)
                if t not in item_dict["perks"]["WeaponPerks"]:
                    item_dict["perks"]["WeaponPerks"][t] = [inventory_socket_object]
                else:
                    item_dict["perks"]["WeaponPerks"][t].append(inventory_socket_object)

        elif socket_category_hash == 4241085061:  # WEAPON PERKS
            socket_indexes = socket_category["socketIndexes"]
            item_dict["perks"]["CuratedRolls"] = []
            for index in socket_indexes:
                weapon_perk = socket_entries[index]
                if "randomizedPlugSetHash" in weapon_perk:
                    plug_set_list = extract_socket_objects(plug_set_dict, weapon_perk, "randomizedPlugSetHash")
                    for item in plug_set_list:
                        t, inventory_result = extract_inventory_item_definition(str(item), inventory_dict, stats_dict)
                        if t == "":
                            continue

                        if t not in item_dict["perks"]["WeaponPerks"]:
                            item_dict["perks"]["WeaponPerks"][t] = [inventory_result]
                        else:
                            item_dict["perks"]["WeaponPerks"][t].append(inventory_result)

                elif "reusablePlugSetHash" in weapon_perk:
                    plug_set_list = extract_socket_objects(plug_set_dict, weapon_perk, "reusablePlugSetHash")
                    for item in plug_set_list:
                        t, inventory_result = extract_inventory_item_definition(str(item), inventory_dict, stats_dict)
                        if t == "":
                            continue

                        if t not in item_dict["perks"]["WeaponPerks"]:
                            item_dict["perks"]["WeaponPerks"][t] = [inventory_result]
                        else:
                            item_dict["perks"]["WeaponPerks"][t].append(inventory_result)

                curated_hash = str(weapon_perk["singleInitialItemHash"])
                t, curated_object = extract_inventory_item_definition(curated_hash, inventory_dict, stats_dict)
                if t == "":
                    continue
                item_dict["perks"]["CuratedRolls"].append(curated_object)

        else:
            continue


def build_weapon_json():
    weapons_dict = {}
    with (
        open(join(RAW, "DestinyInventoryItemDefinition.json"), "rb") as inventory_rf,
        open(join(RAW, "DestinyInventoryItemDefinition.json"), "rb") as inventory1_rf,
        open(join(RAW, "DestinyStatDefinition.json"), "rb") as stats_rf,
        open(join(RAW, "DestinyPlugSetDefinition.json"), "rb") as plug_set_rf,
        open(join(DATA, "weapons.json"), "wb") as weapons_wf,
    ):
        stats_dict = loads(stats_rf.read())
        plug_set_dict = loads(plug_set_rf.read())
        inventory_dict = loads(inventory1_rf.read())

        for k, v in kvitems(inventory_rf, ""):
            itemType = v["itemType"]

            if itemType is not None and itemType == 3 and k == "55393445":
                item_dict = {}
                weapons_dict[k] = item_dict

                item_dict["name"] = v["displayProperties"]["name"]
                item_dict["icon"] = v["displayProperties"]["icon"]
                item_dict["screenshot"] = v["screenshot"]
                item_dict["watermark"] = v["iconWatermark"]
                item_dict["weapon_type"] = v["itemTypeDisplayName"]
                item_dict["flavor_text"] = v["flavorText"]
                item_dict["tier_type"] = v["inventory"]["tierTypeName"]
                item_dict["adept"] = v["isAdept"]
                item_dict["holo_foil"] = v["isHolofoil"]

                process_equipping_block(item_dict, v)
                process_investment_stats(v, item_dict, stats_dict)
                process_sockets(v, item_dict, plug_set_dict, inventory_dict, stats_dict)

        weapons_wf.write(dumps(weapons_dict, option=OPT_INDENT_2))


async def main():
    # create_directories()
    # create_csv_for_weapon_armor_sockets()
    # create_csv_for_stats_plugsets_damagetypes()
    build_weapon_json()


if __name__ == "__main__":
    run(main())
