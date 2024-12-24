import unittest
from datetime import timedelta

from pyomodel.actions.empire_control import EmpireControl
from pyomodel.actions.planet_control import PlanetControl
from pyomodel.core.gamestate import GameState
from pyomodel.core.technologies import Technologies
from pyomodel.simulation.engine import GameEngine
from pyomodel.simulation.server_env import SimulatedGameEnv
from tests.test_env_obj_builder import build_rich_starter_empire, build_rich_empire_with_buildings


class TestEngineResearch(unittest.TestCase):

    def test_building(self):
        game_env = SimulatedGameEnv()

        empire = build_rich_empire_with_buildings()
        game_state = GameState(empires=[empire])
        game_engine = GameEngine()
        game_engine.setup(game_env, game_state)
        empire_control = EmpireControl(empire)

        technology_to_research = Technologies.energy_technology
        assert empire.technology[technology_to_research] == 0

        # start building
        empire_control.start_research(technology_to_research)

        # pass enough time
        game_env.pass_time(time_passed=timedelta(hours=10))
        game_engine.update_state()

        assert empire.technology[technology_to_research] == 1