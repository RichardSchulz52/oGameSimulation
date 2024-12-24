import unittest
from datetime import timedelta

from pyomodel.actions.planet_control import PlanetControl
from pyomodel.core.buildings import Buildings
from pyomodel.core.gamestate import GameState
from pyomodel.simulation.engine import GameEngine
from pyomodel.simulation.server_env import SimulatedGameEnv
from tests.test_env_obj_builder import build_rich_starter_empire


class TestEngineBuilding(unittest.TestCase):

    def test_building(self):
        game_env = SimulatedGameEnv()

        empire = build_rich_starter_empire()
        game_state = GameState(empires=[empire])
        game_engine = GameEngine()
        game_engine.setup(game_env, game_state)
        main_planet_control = PlanetControl(empire.main_planet)

        building_to_upgrade = Buildings.metal_mine
        assert empire.main_planet.buildings[building_to_upgrade] == 0

        # start building
        main_planet_control.start_building_upgrade(building_to_upgrade)

        # pass enough time
        game_env.pass_time(time_passed=timedelta(hours=1))
        game_engine.update_state()

        assert empire.main_planet.buildings[building_to_upgrade] == 1


    def test_build_building_produces_more_than_finished_building(self):
        game_env = SimulatedGameEnv()

        empire = build_rich_starter_empire()
        game_state = GameState(empires=[empire])
        game_engine = GameEngine()
        game_engine.setup(game_env, game_state)
        main_planet_control = PlanetControl(empire.main_planet)

        building_to_upgrade = Buildings.metal_mine
        assert empire.main_planet.buildings[building_to_upgrade] == 0

        # start building
        main_planet_control.start_building_upgrade(building_to_upgrade)

        # pass enough time
        game_env.pass_time(time_passed=timedelta(hours=1))
        game_engine.update_state()

        assert empire.main_planet.buildings[building_to_upgrade] == 1



