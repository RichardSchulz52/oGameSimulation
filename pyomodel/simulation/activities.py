from datetime import datetime

from pyomodel.core.buildings import Building
from pyomodel.core.empire import Empire
from pyomodel.core.materials import Materials
from pyomodel.core.planet import Planet
from pyomodel.core.technologies import Technology
from pyomodel.simulation.engine import GameEngine, UpdateEvent
from pyomodel.simulation.server_env import GameEnv


class GameActivity:
    def __init__(self):
        self.game_env: GameEnv = GameEnv()
        self.game_engine: GameEngine = GameEngine()
        self.start_time = self.game_env.get_current_time()
        self.update_event = self._update_event()
        self.game_engine.add_update_event(self.update_event)

    def _update_event(self):
        return UpdateEvent(self.finish_time(), self.update_when_finished)

    def finish_time(self):
        raise NotImplementedError("Implement in child class")

    def update_when_finished(self):
        raise NotImplementedError("Implement in child class")

    def abort(self):
        self.game_engine.remove_update(self.update_event)


class BuildingUpgrade(GameActivity):
    def __init__(self, planet: Planet, asset: Building):
        self.planet = planet
        self.asset = asset
        super().__init__()

    def upgrade_cost(self) -> Materials:
        return self.asset.cost_for_next_level()

    def finish_time(self) -> datetime:
        return self.start_time + self.asset.next_level_delivery_time()

    def update_when_finished(self):
        global building_upgrades
        del building_upgrades[self.planet]
        self.planet.rise_building_level(self.asset.name)

    def abort(self):
        super().abort()
        global building_upgrades
        del building_upgrades[self.planet]
        update_cost = self.asset.cost_for_next_level()
        self.planet.add_materials(update_cost)


class TechnologyResearch(GameActivity):
    def __init__(self, technology: Technology, empire : Empire, planet: Planet):
        self.technology = technology
        self.empire = empire
        self.planet = planet
        super().__init__()

    def finish_time(self) -> datetime:
        return self.start_time + self.technology.next_level_delivery_time()

    def update_when_finished(self):
        global technology_researches
        del technology_researches[self.empire]
        self.empire.raise_technology_level(self.technology.name)

    def abort(self):
        super().abort()
        global technology_researches
        del technology_researches[self.empire]
        update_cost = self.technology.cost_for_next_level()
        self.planet.add_materials(update_cost)


building_upgrades: dict[Planet, BuildingUpgrade] = dict() #TODO make proper singleton class
technology_researches: dict[Empire, TechnologyResearch] = dict()  #TODO make proper singleton class

def start_building_upgrade(building_upgrade: BuildingUpgrade):
    global building_upgrades
    planet = building_upgrade.planet
    if planet in building_upgrades:
        raise Exception("Building already in progress")
    building_upgrades[planet] = building_upgrade


def get_building_upgrade(planet: Planet):
    global building_upgrades
    if planet in building_upgrades:
        return building_upgrades[planet]
    else:
        return None



def start_technology_research(technology_research: TechnologyResearch):
    global technology_researches
    empire = technology_research.empire
    if empire in technology_researches:
        raise Exception("Research already in progress")
    technology_researches[empire] = technology_research


def get_technology_research(empire: Empire):
    global technology_researches
    if empire in technology_researches:
        return technology_researches[empire]
    else:
        return None
