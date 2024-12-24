from pyomodel.core.assets import AssetLevelTracker
from pyomodel.core.materials import Materials
from pyomodel.core.buildings import Buildings, Building
from pyomodel.core.spacecraft import Spacecraft
from pyomodel.core.technologies import Technologies


basic_metal_income = 30
basic_crystal_income = 20

class Planet:
    def __init__(self, name='Main Planet', size=200, temperature=50, materials: Materials = None,
                 buildings: AssetLevelTracker = None):
        self.name = name
        self.size = size
        self.temperature = temperature

        if materials is None:
            self.materials = Materials(0, 0, 0)
        else:
            self.materials = materials
        if buildings is None:
            self.buildings: AssetLevelTracker = AssetLevelTracker(Buildings())
        else:
            self.buildings = buildings
        self.orbit: dict[str:int] = dict()

    def level_of_building(self, building):
        return self.buildings[building]

    def numbers_in_orbit(self, spacecraft):
        if spacecraft not in self.orbit:
            return 0
        return self.orbit[spacecraft]

    def material_production_per_hour(self) -> Materials:
        metal_mine_level = self.level_of_building(Buildings.metal_mine)
        metal_production = 30 * metal_mine_level * pow(1.1, metal_mine_level) + basic_metal_income  # TODO reserch and plasma tecnology

        crystal_mine_level = self.level_of_building(Buildings.crystal_mine)
        crystal_production = 20 * crystal_mine_level * pow(1.1, crystal_mine_level) + basic_crystal_income # TODO reserch and plasma tecnology

        deuterium_synthesizer_level = self.level_of_building(Buildings.deuterium_synthesizer)
        deuterium_production = (10 * deuterium_synthesizer_level * pow(1.1, deuterium_synthesizer_level)) * (
                1.36 - 0.004 * self.temperature)
        deuterium_consumption = 0  # TODO fusion reactor
        deuterium_balance = deuterium_production - deuterium_consumption

        return Materials(metal_production, crystal_production, deuterium_balance)

    def energy_balance(self):
        consumption = self.total_energy_consumption()
        production = self.total_energy_production()
        return production - consumption

    def total_energy_consumption(self) -> float:
        energy_consumers = Buildings.energy_base_consumption.keys()
        all_consumptions = [self.energy_consumption_for(c) for c in energy_consumers]
        return sum(all_consumptions)

    def energy_consumption_for(self, c):
        return self.current_building(c).energy_consumption()

    def current_building(self, name) -> Building:
        level = self.level_of_building(name)
        return Building(name, level, self.buildings)

    def total_energy_production(self) -> float:
        solar_plant_output = self.solar_plant_output()
        fusion_reactor_output = self.fusion_reactor_output()
        satellites_output = self.total_solar_satellite_output()
        return solar_plant_output * fusion_reactor_output * satellites_output

    def solar_plant_output(self):
        level_solar_plant = self.level_of_building(Buildings.solar_plant)
        return 20 * level_solar_plant * pow(1.1, level_solar_plant)

    def fusion_reactor_output(self):
        level_fusion_reactor = self.level_of_building(Buildings.fusion_reactor)
        energy_technology_level = self.level_of_building(Technologies.energy_technology)
        return 30 * level_fusion_reactor * pow((1.05 + (0.01 * energy_technology_level)), level_fusion_reactor)

    def total_solar_satellite_output(self):
        number_of_satellites = self.numbers_in_orbit(Spacecraft.solar_satellite)
        return self.solar_satellite_output() * number_of_satellites

    def solar_satellite_output(self):
        return (self.temperature + 160) / 6

    def current_materials(self) -> Materials:
        return self.materials

    def remove_materials(self, upgrade_costs: Materials):
        self.materials = self.materials - upgrade_costs

    def add_materials(self, materials: Materials):
        self.materials = self.materials + materials

    def rise_building_level(self, name):
        self.buildings.raise_level(name)
