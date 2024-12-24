import unittest

from pyomodel.actions.empire_control import EmpireControl
from pyomodel.core.technologies import Technologies
from tests.test_env_obj_builder import build_rich_empire_with_buildings


class TestEmpireControl(unittest.TestCase):

    def test_start_research(self):
        empire = build_rich_empire_with_buildings()
        empire_control = EmpireControl(empire)
        empire_control.start_research(Technologies.energy_technology)
        assert empire_control.technology_research is not None

