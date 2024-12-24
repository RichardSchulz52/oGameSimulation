from pyomodel.actions.exceptions import InvalidAction
from pyomodel.actions.planet_control import PlanetControl
from pyomodel.core.buildings import Buildings
from pyomodel.core.empire import Empire
from pyomodel.core.planet import Planet
from pyomodel.core.technologies import Technology
from pyomodel.simulation.activities import TechnologyResearch, get_technology_research, start_technology_research


class EmpireControl:
    def __init__(self, empire: Empire):
        self.empire: Empire = empire
        self.active_planet: Planet = empire.main_planet  # set only by set_active_planet()
        self.active_planet_control: PlanetControl = PlanetControl(self.active_planet)  # set only by set_active_planet()

    def set_active_planet(self, planet):
        if planet not in self.empire.planets:
            raise InvalidAction(f"Can't set the planet {planet} to active, because its not part of the empire.")
        self.active_planet = planet
        self.active_planet_control = PlanetControl(self.active_planet)

    def start_research(self, technology_name):
        current_technology_level = self.empire.get_technology_level(technology_name)
        technology = Technology(technology_name, current_technology_level, self.active_planet.buildings)
        research_costs = technology.cost_for_next_level()

        self.active_planet_control.validate_liquidity(research_costs)
        if get_technology_research(self.empire) is not None:
            raise InvalidAction("A Technology is already researched")
        research_lab_level = self.active_planet.current_building(Buildings.research_lab).level
        if research_lab_level == 0:
            raise InvalidAction("There is no research lab on the active planet")
        research = TechnologyResearch(technology, self.empire, self.active_planet)
        start_technology_research(research)


    def aboard_technology_research(self):
        research = get_technology_research(self.empire)
        if research is None:
            raise InvalidAction("Can't aboard anything")
        research.abort()




