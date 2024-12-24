import unittest

from pyomodel.core.materials import Materials


class TestMaterials(unittest.TestCase):
    def test_multiply(self):
        original = Materials(5,3,4)
        times_two = original * 2
        assert times_two.metal == 10
        assert times_two.crystal == 6
        assert times_two.deuterium == 8

    def test_r_multiply(self):
        original = Materials(5,3,4)
        times_two = 2 * original
        assert times_two.metal == 10
        assert times_two.crystal == 6
        assert times_two.deuterium == 8

    def test_addition(self):
        one = Materials(5, 3, 4)
        two = Materials(1, 2, 3)
        added = one + two
        assert added.metal == 6
        assert added.crystal == 5
        assert added.deuterium == 7

    def test_subtraction(self):
        one = Materials(5, 3, 4)
        two = Materials(1, 2, 3)
        added = one - two
        assert added.metal == 4
        assert added.crystal == 1
        assert added.deuterium == 1

    def test_all_less_equal(self):
        bigger = Materials(5, 3, 4)
        smaller = Materials(2, 1, 3)
        assert not bigger.all_less_or_equal(smaller)
        assert smaller.all_less_or_equal(bigger)


