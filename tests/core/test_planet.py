import unittest

from pyomodel.core.assets import AssetDoesNotExist
from pyomodel.core.buildings import Buildings
from pyomodel.core.planet import Planet


class TestPlanet(unittest.TestCase):

    def test_initial_asset_level(self):
        p = Planet()
        lvl = p.level_of_building(Buildings.crystal_storage)
        assert lvl == 0

    def test_asset_level_upgrade(self):
        p = Planet()
        p.rise_building_level(Buildings.crystal_storage)
        lvl = p.level_of_building(Buildings.crystal_storage)
        assert lvl == 1

    def test_invalid_asset_rejection(self):
        p = Planet()
        self.assertRaises(AssetDoesNotExist, p.rise_building_level, "not_an_asset")





