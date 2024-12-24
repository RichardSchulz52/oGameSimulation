from datetime import datetime, timedelta


class GameEnv:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameEnv, cls).__new__(cls)
        return cls.instance

    def get_current_time(self) -> datetime:
        return datetime.now()

    def __init__(self):
        self.start_time = datetime.now()


class SimulatedGameEnv(GameEnv):

    def __init__(self):
        super().__init__()
        self.time_passed = timedelta(seconds=0)

    def pass_time(self, time_passed: timedelta):
        self.time_passed += time_passed

    def get_current_time(self):
        return self.start_time + self.time_passed
