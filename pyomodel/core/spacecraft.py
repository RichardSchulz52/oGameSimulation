from pyomodel.core.materials import Materials


class Spacecraft:
    """
    All string attributes on the class level represent a buildable spacecraft.
    Therefore, string other than spacecraft names mustn't be present here.
    """

    solar_satellite = 'solar_satellite'

    cost = {
        solar_satellite: Materials(0, 2000, 500),
    }