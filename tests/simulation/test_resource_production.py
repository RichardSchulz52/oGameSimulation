import unittest
from datetime import timedelta

from pyomodel.core.buildings import Buildings
from pyomodel.core.gamestate import GameState
from pyomodel.core.planet import basic_metal_income, basic_crystal_income
from pyomodel.simulation.engine import GameEngine
from pyomodel.simulation.server_env import SimulatedGameEnv
from tests.test_env_obj_builder import build_starter_empire


class TestResourceProduction(unittest.TestCase):

    def test_base_production(self):
        game_env = SimulatedGameEnv()
        empire = build_starter_empire()
        game_state = GameState(empires=[empire])
        engine = GameEngine()
        engine.setup(game_env, game_state)

        start_materials = empire.main_planet.materials
        game_env.pass_time(timedelta(hours=1))
        engine.update_state()
        current_materials = empire.main_planet.materials
        assert not current_materials.all_less_or_equal(start_materials)
        assert current_materials.metal - start_materials.metal == basic_metal_income
        assert current_materials.crystal - start_materials.crystal == basic_crystal_income

    def test_greater_mine_greater_production(self):
        game_env = SimulatedGameEnv()
        empire = build_starter_empire()
        empire2 = build_starter_empire({Buildings.metal_mine: 1})
        game_state = GameState(empires=[empire, empire2])
        engine = GameEngine()
        engine.setup(game_env, game_state)

        assert empire.main_planet.materials.metal == empire2.main_planet.materials.metal
        game_env.pass_time(timedelta(hours=1))
        engine.update_state()
        assert empire.main_planet.materials.metal < empire2.main_planet.materials.metal
