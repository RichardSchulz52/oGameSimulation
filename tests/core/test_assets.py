import unittest

from pyomodel.core.assets import AssetLevelTracker, AssetDoesNotExist
from pyomodel.core.buildings import Buildings


class TestLevelTracker(unittest.TestCase):
    def test_level_tracker_item_access(self):
        level_tracker = AssetLevelTracker(Buildings())
        assert level_tracker[Buildings.solar_plant] == 0

    def test_rise_level(self):
        level_tracker = AssetLevelTracker(Buildings())
        level_tracker.raise_level(Buildings.fusion_reactor)
        assert level_tracker[Buildings.fusion_reactor] == 1

    def test_double_rise_level(self):
        level_tracker = AssetLevelTracker(Buildings())
        level_tracker.raise_level(Buildings.fusion_reactor)
        level_tracker.raise_level(Buildings.fusion_reactor)
        assert level_tracker[Buildings.fusion_reactor] == 2

    def test_item_validation(self):
        level_tracker = AssetLevelTracker(Buildings())
        self.assertRaises(AssetDoesNotExist, lambda: level_tracker['i_do_not_exist'])

    def test_item_setting_forbidden(self):
        level_tracker = AssetLevelTracker(Buildings())
        def assign_item():
            level_tracker[Buildings.fusion_reactor] = 6
        self.assertRaises(NotImplementedError, assign_item)

