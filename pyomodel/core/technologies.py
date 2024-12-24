from datetime import timedelta

from pyomodel.core.assets import AssetSupplier, Asset, AssetLevelTracker
from pyomodel.core.buildings import Buildings
from pyomodel.core.materials import Materials


class Technologies(AssetSupplier):
    """
    All string attributes on the class level represent a technology.
    Therefore, string other than technology names mustn't be present here.
    """
    espionage_technology = 'espionage_technology'
    computer_technology = 'computer_technology'
    weapons_technology = 'weapons_technology'
    shield_technology = 'shield_technology'
    armour_technology = 'armour_technology'
    energy_technology = 'energy_technology'
    hyperspace_technology = 'hyperspace_technology'
    combustion_drive = 'combustion_drive'
    impulsive_drive = 'impulsive_drive'
    hyperspace_drive = 'hyperspace_drive'
    laser_technology = 'laser_technology'
    ion_technology = 'ion_technology'
    plasma_technology = 'plasma_technology'
    intergalactic_research_network = 'intergalactic_research_network'
    astrophysics = 'astrophysics'
    graviton_technology = 'graviton_technology'
    # TODO production maximization ?

    base_cost = {
        energy_technology: Materials(0, 800, 400),
        combustion_drive: Materials(200, 0, 300),
        laser_technology: Materials(100, 50, 0),
        ion_technology: Materials(500, 150, 50),
        hyperspace_technology: Materials(0, 2000, 1000),
        plasma_technology: Materials(1000, 2000, 500),
        espionage_technology: Materials(100, 500, 100),
        computer_technology: Materials(0, 200, 300),
        astrophysics: Materials(2000, 4000, 2000),
        graviton_technology: Materials(0,0,0),
        weapons_technology: Materials(400,100,0),
        shield_technology: Materials(100, 300, 0),
        armour_technology: Materials(500, 0, 0),
        impulsive_drive: Materials(1000, 2000, 300),
        hyperspace_drive: Materials(5000, 10000, 3000),
        intergalactic_research_network: Materials(120000, 200000, 80000),
    }

    level_cost_base = {
        astrophysics: 1.75,
        graviton_technology: 3,
    }


class Technology(Asset):
    def __init__(self, name, level, planet_buildings: AssetLevelTracker = None):
        super().__init__(name, level)
        self.base_cost = Technologies.base_cost[self.name]
        self.planet_buildings = planet_buildings

    def cost_for_level(self, level) -> Materials:
        base = self._level_base_cost()
        return self.base_cost * pow(base, level)

    def delivery_time(self, level) -> timedelta:
        cost = self.cost_for_level(self.level)
        research_lab_level = self.planet_buildings[Buildings.research_lab]
        upgrade_hours = (cost.metal + cost.crystal) / (1000 * (1 + research_lab_level))
        return timedelta(hours=upgrade_hours)

    def _level_base_cost(self):
        if self.name in Buildings.level_cost_base:
            return Buildings.level_cost_base[self.name]
        else:
            return 2










