from asyncio import run
from os.path import join, exists
from loguru import logger

import orjson

from http_io import download_all
from models import ManifestRoot

ROOT = "G:\\"
ASSETS = join(ROOT, "Assets")
RAW = join(ASSETS, "Raw")
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


async def main():
    manifest = get_manifest_model()
    cache_version(manifest.Response.version)
    jwccp_lst = [(join(RAW, f'{x}.json'), y) for x, y in manifest.to_list('en')]
    await download_all(jwccp_lst)

if __name__ == '__main__':
    run(main())