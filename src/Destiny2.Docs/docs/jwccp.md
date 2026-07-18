---
layout: doc
---

# Json World Component Content Paths

## Download the Data:

```python
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
```

### HTTP_IO

```python
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
```

### Models

```python
from typing import List, Tuple
from unittest import case

from pydantic import BaseModel, Field, ConfigDict


class Destiny2Tables(BaseModel):
    DestinyArtDyeChannelDefinition: str
    DestinyArtDyeReferenceDefinition: str
    DestinyPlaceDefinition: str
    DestinyActivityDefinition: str
    DestinyActivityTypeDefinition: str
    DestinyClassDefinition: str
    DestinyGenderDefinition: str
    DestinyInventoryBucketDefinition: str
    DestinyRaceDefinition: str
    DestinyUnlockDefinition: str
    DestinyStatGroupDefinition: str
    DestinyProgressionMappingDefinition: str
    DestinyFactionDefinition: str
    DestinyVendorGroupDefinition: str
    DestinyRewardSourceDefinition: str
    DestinyUnlockValueDefinition: str
    DestinyRewardMappingDefinition: str
    DestinyItemCategoryDefinition: str
    DestinyDamageTypeDefinition: str
    DestinyActivityModeDefinition: str
    DestinyMedalTierDefinition: str
    DestinyAchievementDefinition: str
    DestinyActivityDifficultyTierCollectionDefinition: str
    DestinyActivityFamilyDefinition: str
    DestinyActivityGraphDefinition: str
    DestinyActivityInteractableDefinition: str
    DestinyActivityLoadoutRestrictionDefinition: str
    DestinyActivitySelectableSkullCollectionDefinition: str
    DestinyActivitySelectableSkullExclusionGroupDefinition: str
    DestinyActivitySkullCategoryDefinition: str
    DestinyActivitySkullCollectionDefinition: str
    DestinyActivitySkullSubcategoryDefinition: str
    DestinyBondDefinition: str
    DestinyCharacterCustomizationCategoryDefinition: str
    DestinyCharacterCustomizationOptionDefinition: str
    DestinyCollectibleDefinition: str
    DestinyDestinationDefinition: str
    DestinyEntitlementOfferDefinition: str
    DestinyEquipableItemSetDefinition: str
    DestinyEquipmentSlotDefinition: str
    DestinyEventCardDefinition: str
    DestinyFireteamFinderActivityGraphDefinition: str
    DestinyFireteamFinderActivitySetDefinition: str
    DestinyFireteamFinderLabelDefinition: str
    DestinyFireteamFinderLabelGroupDefinition: str
    DestinyFireteamFinderOptionDefinition: str
    DestinyFireteamFinderOptionGroupDefinition: str
    DestinyIconDefinition: str
    DestinyStatDefinition: str
    DestinyInventoryItemDefinition: str
    DestinyInventoryItemLiteDefinition: str
    DestinyItemFilterDefinition: str
    DestinyItemTierTypeDefinition: str
    DestinyLoadoutColorDefinition: str
    DestinyLoadoutIconDefinition: str
    DestinyLoadoutNameDefinition: str
    DestinyLocationDefinition: str
    DestinyLoreDefinition: str
    DestinyMaterialRequirementSetDefinition: str
    DestinyMetricDefinition: str
    DestinyObjectiveDefinition: str
    DestinySandboxPerkDefinition: str
    DestinyPlatformBucketMappingDefinition: str
    DestinyPlugSetDefinition: str
    DestinyPowerCapDefinition: str
    DestinyPresentationNodeDefinition: str
    DestinyProgressionDefinition: str
    DestinyProgressionLevelRequirementDefinition: str
    DestinyRecordDefinition: str
    DestinyRewardAdjusterPointerDefinition: str
    DestinyRewardAdjusterProgressionMapDefinition: str
    DestinyRewardItemListDefinition: str
    DestinySackRewardItemListDefinition: str
    DestinySandboxPatternDefinition: str
    DestinySeasonDefinition: str
    DestinySeasonPassDefinition: str
    DestinySocialCommendationDefinition: str
    DestinySocketCategoryDefinition: str
    DestinySocketTypeDefinition: str
    DestinyTraitDefinition: str
    DestinyUnlockCountMappingDefinition: str
    DestinyUnlockEventDefinition: str
    DestinyUnlockExpressionMappingDefinition: str
    DestinyVendorDefinition: str
    DestinyMilestoneDefinition: str
    DestinyActivityModifierDefinition: str
    DestinyReportReasonCategoryDefinition: str
    DestinyArtifactDefinition: str
    DestinyBreakerTypeDefinition: str
    DestinyChecklistDefinition: str
    DestinyEnergyTypeDefinition: str
    DestinySocialCommendationNodeDefinition: str
    DestinyGuardianRankDefinition: str
    DestinyGuardianRankConstantsDefinition: str
    DestinyLoadoutConstantsDefinition: str
    DestinyFireteamFinderConstantsDefinition: str
    DestinyGlobalConstantsDefinition: str
    DestinyInventoryItemConstantsDefinition: str

class JsonWorldComponentContentPaths(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    en: Destiny2Tables
    fr: Destiny2Tables
    es: Destiny2Tables
    esMx: Destiny2Tables = Field(alias="es-mx")
    de: Destiny2Tables
    it: Destiny2Tables
    ja: Destiny2Tables
    ptBr: Destiny2Tables = Field(alias="pt-br")
    ru: Destiny2Tables
    pl: Destiny2Tables
    ko: Destiny2Tables
    zhCht: Destiny2Tables = Field(alias="zh-cht")
    zhChs: Destiny2Tables = Field(alias="zh-chs")

    def keys(self, key: str):
        match key:
            case "en":
                return list(self.en.model_dump().keys())
            case "fr":
                return list(self.fr.model_dump().keys())
            case "es":
                return list(self.es.model_dump().keys())
            case "esMx":
                return list(self.esMx.model_dump().keys())
            case "de":
                return list(self.de.model_dump().keys())
            case "it":
                return list(self.it.model_dump().keys())
            case "ja":
                return list(self.ja.model_dump().keys())
            case "ptBr":
                return list(self.ptBr.model_dump().keys())
            case "ru":
                return list(self.ru.model_dump().keys())
            case "pl":
                return list(self.pl.model_dump().keys())
            case "ko":
                return list(self.ko.model_dump().keys())
            case "zhCht":
                return list(self.zhCht.model_dump().keys())
            case "zhChs":
                return list(self.zhChs.model_dump().keys())
        return None

    def values(self, key: str):
        match key:
            case "en":
                return list(self.en.model_dump().values())
            case "fr":
                return list(self.fr.model_dump().values())
            case "es":
                return list(self.es.model_dump().values())
            case "esMx":
                return list(self.esMx.model_dump().values())
            case "de":
                return list(self.de.model_dump().values())
            case "it":
                return list(self.it.model_dump().values())
            case "ja":
                return list(self.ja.model_dump().values())
            case "ptBr":
                return list(self.ptBr.model_dump().values())
            case "ru":
                return list(self.ru.model_dump().values())
            case "pl":
                return list(self.pl.model_dump().values())
            case "ko":
                return list(self.ko.model_dump().values())
            case "zhCht":
                return list(self.zhCht.model_dump().values())
            case "zhChs":
                return list(self.zhChs.model_dump().values())
        return None

    def to_list(self, key: str):

        match key:
            case "en":
                return list(self.en.model_dump().items())
            case "fr":
                return list(self.fr.model_dump().items())
            case "es":
                return list(self.es.model_dump().items())
            case "esMx":
                return list(self.esMx.model_dump().items())
            case "de":
                return list(self.de.model_dump().items())
            case "it":
                return list(self.it.model_dump().items())
            case "ja":
                return list(self.ja.model_dump().items())
            case "ptBr":
                return list(self.ptBr.model_dump().items())
            case "ru":
                return list(self.ru.model_dump().items())
            case "pl":
                return list(self.pl.model_dump().items())
            case "ko":
                return list(self.ko.model_dump().items())
            case "zhCht":
                return list(self.zhCht.model_dump().items())
            case "zhChs":
                return list(self.zhChs.model_dump().items())
        return None

    def to_dict(self, key: str):
        match key:
            case "en":
                return [{'name': key, 'url': value} for key, value in self.en.model_dump().items()]
            case "fr":
                return [{'name': key, 'url': value} for key, value in self.fr.model_dump().items()]
            case "es":
                return [{'name': key, 'url': value} for key, value in self.es.model_dump().items()]
            case "esMx":
                return [{'name': key, 'url': value} for key, value in self.esMx.model_dump().items()]
            case "de":
                return [{'name': key, 'url': value} for key, value in self.de.model_dump().items()]
            case "it":
                return [{'name': key, 'url': value} for key, value in self.it.model_dump().items()]
            case "ja":
                return [{'name': key, 'url': value} for key, value in self.ja.model_dump().items()]
            case "ptBr":
                return [{'name': key, 'url': value} for key, value in self.ptBr.model_dump().items()]
            case "ru":
                return [{'name': key, 'url': value} for key, value in self.ru.model_dump().items()]
            case "pl":
                return [{'name': key, 'url': value} for key, value in self.pl.model_dump().items()]
            case "ko":
                return [{'name': key, 'url': value} for key, value in self.ko.model_dump().items()]
            case "zhCht":
                return [{'name': key, 'url': value} for key, value in self.zhCht.model_dump().items()]
            case "zhChs":
                return [{'name': key, 'url': value} for key, value in self.zhChs.model_dump().items()]
        return None

class Response(BaseModel):
    version: str
    jsonWorldComponentContentPaths: JsonWorldComponentContentPaths

class ManifestRoot(BaseModel):
    Response: Response

    def to_list(self, key: str):
        return self.Response.jsonWorldComponentContentPaths.to_list(key)

    def to_dict(self, key: str):
        return self.Response.jsonWorldComponentContentPaths.to_dict(key)
```

### Last Commit
```bash
Updating 1fe86f4..edd591a
Fast-forward
 .gitignore                             |   1 +
 src/Destiny2.Jwccp/http_io/__init__.py |  36 ++++
 src/Destiny2.Jwccp/main.py             |  50 +++++
 src/Destiny2.Jwccp/models/__init__.py  | 256 ++++++++++++++++++++++
 src/Destiny2.Jwccp/pyproject.toml      |  11 +
 src/Destiny2.Jwccp/uv.lock             | 383 +++++++++++++++++++++++++++++++++
 src/Destiny2.Manifest/main.py          |  23 +-
```