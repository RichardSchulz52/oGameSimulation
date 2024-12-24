import unittest

from pyomodel.actions.exceptions import InvalidAction
from pyomodel.actions.planet_control import PlanetControl
from pyomodel.core.buildings import Buildings, Building
from pyomodel.core.materials import Materials
from pyomodel.core.planet import Planet
from pyomodel.core.technologies import Technologies
from pyomodel.simulation.server_env import GameEnv, SimulatedGameEnv
from tests.test_env_obj_builder import build_rich_starter_empire, build_starter_empire


class TestPlanetControl(unittest.TestCase):
    def test_building(self):
        planet = Planet(materials=Materials(1000, 1000, 1000))
        game_env = SimulatedGameEnv()
        planet_control = PlanetControl(planet)
        planet_control.start_building_upgrade(Buildings.solar_plant)
        assert planet_control._building_production is not None
        assert planet_control._building_production.planet == planet
        assert planet_control._building_production.asset.name == Buildings.solar_plant
        assert planet_control._building_production.start_time == game_env.start_time

    def test_insufficient_resources_for_building(self):
        planet_control = PlanetControl(Planet())
        self.assertRaises(InvalidAction, planet_control.start_building_upgrade, Buildings.solar_plant)

    def test_resource_consumption_of_building(self):
        start_materials = Materials(1000, 1000, 1000)
        planet_control = PlanetControl(Planet(materials=start_materials))
        planet_control.start_building_upgrade(Buildings.solar_plant)
        assert planet_control.planet.materials.all_less_or_equal(start_materials)

    def test_unable_research_no_lab(self):
        empire = build_rich_starter_empire()
        planet_control = PlanetControl(empire.main_planet)
        self.assertRaises(InvalidAction, planet_control.start_research, Technologies.energy_technology)

    def test_unable_research_upgrade_lab(self):
        empire = build_starter_empire()
        planet_control = PlanetControl(empire.main_planet)
        self.assertRaises(InvalidAction, planet_control.start_research, Technologies.energy_technology)
