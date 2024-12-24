from pyomodel.actions.exceptions import InvalidAction
from pyomodel.core.materials import Materials
from pyomodel.core.planet import Planet
from pyomodel.simulation.activities import BuildingUpgrade, start_building_upgrade, get_building_upgrade


class PlanetControl:
    def __init__(self, planet: Planet):
        self.planet: Planet = planet

    def start_building_upgrade(self, building_name: str):
        building_production: BuildingUpgrade = self._upgrade_building(building_name)
        start_building_upgrade(building_production)

    def aboard_building(self):
        building_production: BuildingUpgrade = get_building_upgrade(self.planet)
        if building_production is None:
            raise InvalidAction("Can't aboard anything")
        building_production.abort()

    def _upgrade_building(self, asset_name):
        current_building = self.planet.current_building(asset_name)
        upgrade_costs = current_building.cost_for_next_level()
        self.validate_liquidity(upgrade_costs)

        current_production = get_building_upgrade(self.planet)
        if current_production is not None:
            raise InvalidAction("Can't build while building is under construction")

        self.planet.remove_materials(upgrade_costs)
        return BuildingUpgrade(self.planet, current_building)

    def validate_liquidity(self, cost: Materials):
        materials_available = self.planet.current_materials()
        if not cost.all_less_or_equal(materials_available):
            raise InvalidAction("Not sufficient resources")

