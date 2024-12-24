import unittest

from pyomodel.core.empire import Empire
from pyomodel.core.planet import Planet
from pyomodel.core.player import Player
from pyomodel.core.technologies import Technologies


class TestEmpire(unittest.TestCase):
    def test_technology_level(self):
        empire = Empire(Player('Karl Martell'), Planet())
        technology_level = empire.get_technology_level(Technologies.energy_technology)
        assert technology_level == 0

    def test_technology_level_raise(self):
        empire = Empire(Player('Karl Martell'), Planet())
        empire.raise_technology_level(Technologies.energy_technology)
        technology_level = empire.get_technology_level(Technologies.energy_technology)
        assert technology_level == 1

