import inspect
from datetime import timedelta

from pyomodel.core.materials import Materials


class AssetDoesNotExist(Exception):
    pass




class AssetSupplier:
    """
    AssetSuppliers have string attributes that represent game assets.
    """

    def fetch_str_attributes(self) -> list[str]:
        attr = dir(type(self))
        return list(filter(lambda x: x[:1] != '_' and type(x) is str, attr))

    def validate_asset_name(self, name):
        valid_attributes = self.fetch_str_attributes()
        if name not in valid_attributes:
            raise AssetDoesNotExist()


class Asset:
    """
    Represents static elements that have a level.
    """

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def cost_for_level(self, level) -> Materials:
        raise NotImplementedError

    def cost_for_next_level(self) -> Materials:
        return self.cost_for_level(self.level + 1)

    def delivery_time(self, level) -> timedelta:
        raise NotImplementedError

    def next_level_delivery_time(self) -> timedelta:
        return self.delivery_time(self.level + 1)


class AssetLevelTracker(dict[str: int]):
    def __init__(self, asset_supplier: AssetSupplier, levels_dict=None):
        if levels_dict is None:
            levels_dict = {}
        super().__init__(**levels_dict)
        self.asset_supplier = asset_supplier

    def __getitem__(self, __key):
        self.asset_supplier.validate_asset_name(__key)
        self.setdefault(__key, 0)
        return super().__getitem__(__key)

    def raise_level(self, __key):
        self.asset_supplier.validate_asset_name(__key)
        self[__key] = self[__key] + 1

    def __setitem__(self, __key, __value):
        caller_method_name = inspect.stack()[1][3]
        only_allowed_caller = self.raise_level.__name__
        if caller_method_name != only_allowed_caller:
            raise NotImplementedError(
                "Setting levels is only allowed in the constructor. Use the raise_level method instead.")
        super().__setitem__(__key, __value)
