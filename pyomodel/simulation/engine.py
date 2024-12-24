from datetime import datetime, timedelta

from pyomodel.core.gamestate import GameState
from pyomodel.simulation.server_env import GameEnv


class UpdateEvent:
    def __init__(self, due_time: datetime, callback):
        self.due_time = due_time
        self.callback = callback

    def is_due(self, current_time):
        return self.due_time < current_time




class GameEngine:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameEngine, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.updates: list[UpdateEvent] = list() if not hasattr(self, "updates") else self.updates
        self.game_env = None if not hasattr(self, "game_env") else self.game_env
        self.game_state = None if not hasattr(self, "game_state") else self.game_state
        self.last_update_time = None if not hasattr(self, "last_update_time") else self.last_update_time

    def setup(self, game_env: GameEnv, game_state: GameState, last_update_time = None):
        self.game_env = game_env
        self.game_state = game_state
        if last_update_time is None:
            self.last_update_time = game_env.start_time
        else:
            self.last_update_time = last_update_time

    def add_update_event(self, update: UpdateEvent):
        self.updates.append(update)
        self.updates.sort(key=lambda x: x.due_time)

    def remove_update(self, update_event):
        self.updates.remove(update_event)

    def update_state(self):
        current_time = self.game_env.get_current_time()
        self.process_update_events(current_time)
        remaining_time = current_time - self.last_update_time
        self.update_produced_resources(remaining_time)

    def process_update_events(self, current_time):
        updates_to_process: list[UpdateEvent] = list(filter(lambda u: u.is_due(current_time), self.updates))
        updates_to_process: list[UpdateEvent] = sorted(updates_to_process, key=lambda x: x.due_time)
        for update in updates_to_process:
            time_passed_for_update = update.due_time - self.last_update_time
            self.update_produced_resources(
                time_passed_for_update)  # IMPROVE: don't do this for all planets. Only affected ones.
            update.callback()
            self.last_update_time = update.due_time
            self.updates.remove(update)


    def update_produced_resources(self, time_passed: timedelta):
        hour_time_passed = (time_passed.total_seconds() / 60) / 60
        all_empires = self.game_state.empires
        for empire in all_empires:
            empires_planets = empire.planets
            for planet in empires_planets:
                production = planet.material_production_per_hour() * hour_time_passed
                planet.add_materials(production)
