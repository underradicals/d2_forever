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
