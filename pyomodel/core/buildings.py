from datetime import timedelta

from pyomodel.core.assets import Asset, AssetSupplier, AssetLevelTracker
from pyomodel.core.materials import Materials


class Buildings(AssetSupplier):
    """
    All string attributes on the class level represent a building.
    Therefore, string other than building names mustn't be present here.
    """
    metal_mine = 'metal_mine'
    crystal_mine = 'crystal_mine'
    deuterium_synthesizer = 'deuterium_synthesizer'
    solar_plant = 'solar_plant'
    # techno_dome = 'techno_dome'
    fusion_reactor = 'fusion_reactor'
    robotics_factory = 'robotics_factory'
    nanite_factory = 'nanite_factory'
    shipyard = 'shipyard'
    metal_storage = 'metal_storage'
    crystal_storage = 'crystal_storage'
    deuterium_tank = 'deuterium_tank'
    research_lab = 'research_lab'
    # terraformer = 'terraformer'
    alliance_depot = 'alliance_depot'
    # space_dock = 'space_dock'
    missile_silo = 'missile_silo'

    base_costs = { # TODO prüfen ob kosten dem lvl 1 entsprechen oder noch verrechnet werden müssen
        metal_mine: Materials(60, 15, 0),
        crystal_mine: Materials(48, 24, 0),
        deuterium_synthesizer: Materials(225, 75, 0),
        solar_plant: Materials(75, 30, 0),
        fusion_reactor: Materials(900, 360, 180),
        robotics_factory: Materials(400, 120, 200),
        nanite_factory: Materials(1000000, 500000, 100000),
        shipyard: Materials(400, 200, 100),
        metal_storage: Materials(1000, 0, 0),
        crystal_storage: Materials(1000, 500, 0),
        deuterium_tank: Materials(1000, 1000, 0),
        research_lab: Materials(200, 400, 200),
        alliance_depot: Materials(20000, 40000, 0),
        missile_silo: Materials(20000, 20000, 1000),
    }

    # other than 2
    level_cost_base = {
        metal_mine: 1.5,
        deuterium_synthesizer: 1.5,
        solar_plant: 1.5,
        crystal_mine: 1.6,
        fusion_reactor: 1.8,
        # space_dock: 5.0
    }

    energy_base_consumption = {
        metal_mine: 10,
        crystal_mine: 10,
        deuterium_synthesizer: 20,
    }


class Building(Asset):

    def __init__(self, name: str, level: int, planet_buildings: AssetLevelTracker = None):
        super().__init__(name, level)
        self.base_cost = Buildings.base_costs[self.name]
        self.planet_buildings = planet_buildings

    def cost_for_level(self, level) -> Materials:
        cost_factor = self.get_level_cost_factor()
        return self.base_cost * pow(cost_factor, self.level)

    def delivery_time(self, level) -> timedelta:
        robotic_factory_level = self.planet_buildings[Buildings.robotics_factory]
        nanite_factory_level = self.planet_buildings[Buildings.nanite_factory]
        return self.building_time(level, robotic_factory_level, nanite_factory_level)

    def building_time(self, level, robotic_factory_level: int = 0, nanite_factory_level: int = 0):
        cost = self.cost_for_level(level)
        time_hours = (cost.metal + cost.crystal) / (
                2500 * (1 + robotic_factory_level) * pow(2, nanite_factory_level))
        return timedelta(hours=time_hours)

    def get_level_cost_factor(self):
        if self.name in Buildings.level_cost_base:
            return Buildings.level_cost_base[self.name]
        else:
            return 2

    def energy_consumption(self):
        base_consumption = Buildings.energy_base_consumption[self.name]
        return base_consumption * self.level * pow(1.1 * self.level)
