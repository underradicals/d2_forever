from asyncio import run, gather
from os import getenv, makedirs
from os.path import join

from httpx import AsyncClient
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

ROOT = "G:\\"
ASSETS = join(ROOT, "Assets_Dev")
MANIFEST_PATH = join(ASSETS, "manifest.json")


def make_dirs():
    makedirs(ASSETS, exist_ok=True)


def get_headers():
    return {"X-Api-Key": getenv('BUNGIE_API_KEY')}


@retry(wait=wait_exponential(multiplier=1, min=4, max=10),
       stop=stop_after_attempt(5),
       reraise=True
       )
async def download(url: str, path: str, client: AsyncClient):
    async with client.stream('GET', url) as response:
        response.raise_for_status()
        try:
            with open(path, 'wb') as file:
                async for chunk in response.aiter_bytes(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    file.write(chunk)
            logger.info("Download successful {}", path)
        except Exception as e:
            logger.error(e)


async def download_all(data_packet: list) -> None:
    custom_headers = get_headers()
    tasks = []
    async with AsyncClient(base_url='https://www.bungie.net', http2=True, follow_redirects=True,
                           headers=custom_headers) as client:
        packets = [[packet[0], packet[1], client] for packet in data_packet]
        for packet in packets:
            tasks.append(download(packet[0], packet[1], client))

        await gather(*tasks)


async def main():
    make_dirs()
    await download_all([["/Platform/Destiny2/Manifest/", MANIFEST_PATH]])


if __name__ == "__main__":
    run(main())
