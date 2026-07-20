import os
import csv
from asyncio import run
from os.path import join, exists
from loguru import logger

import orjson

from http_io import download_all
from models import ManifestRoot

ROOT = "G:\\"
ASSETS = join(ROOT, "Assets_Dev")
DATA = join(ASSETS, "Data")
RAW = join(DATA, "Raw")
MANIFEST_PATH = join(ASSETS, "manifest.json")

def get_manifest():
    with open(MANIFEST_PATH, "rb") as manifest_file:
        return orjson.loads(manifest_file.read())

def get_manifest_model():
    manifest_dict = get_manifest()
    m = ManifestRoot(**manifest_dict)
    logger.info(f"Manifest root loaded: {len(manifest_dict)} keys")
    return m

def cache_version(manifest_version: str):
    v_path = join(ASSETS, "manifest_version.ini")
    version = ''
    if exists(v_path):
        with open(v_path, "r", encoding='UTF-8') as v_file:
            txt = v_file.read()
            split_version = txt.split(":")[1]
            version = split_version.strip()
    if version != manifest_version:
        logger.info(f"Manifest version has changed: {version}")
        with open(join(ASSETS, "manifest_version.ini"), "w") as ini_file:
            ini_file.write("Version: " + manifest_version)
            logger.info(f"Manifest version was updated: {version}")
            return
    else:
        logger.info(f"Manifest version has not changed: {version}")

def create_directories():
    os.makedirs(RAW, exist_ok=True)


def create_keys(table_names: list[str]):
    name_list = []
    with open(join(ASSETS, "table_names.csv"), 'w', encoding='UTF-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['id', 'name'])
        for index, name in enumerate(table_names):
            name_list.append((index, name))
        csv_writer.writerows(name_list)

async def main():
    create_directories()
    manifest = get_manifest_model()
    cache_version(manifest.Response.version)
    create_keys(manifest.Response.jsonWorldComponentContentPaths.keys('en'))
    jwccp_lst = [(join(RAW, f'{x}.json'), y) for x, y in manifest.to_list('en')]
    await download_all(jwccp_lst)

if __name__ == '__main__':
    run(main())