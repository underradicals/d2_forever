from asyncio import gather
from os import getenv

from httpx import AsyncClient
from loguru import logger
from tenacity import retry, wait_exponential, stop_after_attempt



def get_headers():
    return {"X-Api-Key": getenv('BUNGIE_API_KEY')}


@retry(wait=wait_exponential(multiplier=1, min=4, max=10),
       stop=stop_after_attempt(5),
       reraise=True
       )
async def download(path: str, url: str, client: AsyncClient):
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
    async with AsyncClient(base_url='https://www.bungie.net', http2=True, follow_redirects=True,
                           headers=custom_headers) as client:
        await gather(*[download(x, y, client) for x, y in data_packet])