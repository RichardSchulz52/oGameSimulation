from pyomodel.core.assets import AssetLevelTracker
from pyomodel.core.buildings import Buildings
from pyomodel.core.empire import Empire
from pyomodel.core.materials import Materials
from pyomodel.core.planet import Planet
from pyomodel.core.player import Player



def build_starter_empire(buildings_dict=None) -> Empire:
    player = Player("Karl Martell")
    buildings = AssetLevelTracker(Buildings(), buildings_dict)
    planet = Planet(buildings=buildings)
    return Empire(player, planet)


def build_rich_starter_empire() -> Empire:
    player = Player("Karl Martell")
    million = 1000000
    planet = Planet(materials=Materials(million, million, million))
    return Empire(player, planet)


def build_rich_empire_with_buildings(all_buildings_on_level=10) -> Empire:
    player = Player("Karl Martell")
    million = 1000000
    buildings_asset_level_tracker = build_all_buildings_level(all_buildings_on_level)
    planet = Planet(materials=Materials(million, million, million), buildings=buildings_asset_level_tracker)
    return Empire(player, planet)


def build_all_buildings_level(level: int) -> AssetLevelTracker:
    building_asset_supplier = Buildings()
    building_names = building_asset_supplier.fetch_str_attributes()
    levels_dict = dict()
    for building_name in building_names:
        levels_dict[building_name] = level
    buildings = AssetLevelTracker(building_asset_supplier, levels_dict)
    return buildings
