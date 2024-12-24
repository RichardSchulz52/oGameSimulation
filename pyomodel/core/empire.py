from pyomodel.core.assets import AssetLevelTracker
from pyomodel.core.planet import Planet
from pyomodel.core.player import Player
from pyomodel.core.technologies import Technologies


class Empire:
    def __init__(self, emperor: Player, main_planet: Planet, colonies: list[Planet] = None):
        self._emperor = emperor
        self.main_planet = main_planet
        self.colonies = colonies
        self.technology = AssetLevelTracker(Technologies())
        if colonies is None:
            self.colonies = []
        self.planets = [main_planet] + self.colonies

    def get_technology_level(self, technology_name):
        return self.technology[technology_name]

    def raise_technology_level(self, technology_name):
        self.technology.raise_level(technology_name)
