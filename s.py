import simpy
import random
from datetime import datetime, timedelta

# Simulation of the day's start
today = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour=0, minute=0, second=0)

class Part(object):
    def __init__(self, part_id, part_type, time_required, dependencies=[]):
        self.part_id = part_id
        self.part_type = part_type  # "MAKE" or "BUY"
        self.time_required = time_required
        self.dependencies = dependencies
        self.is_ready = False if dependencies else True

    def __repr__(self):
        return f"Part ID: {self.part_id}, Type: {self.part_type}, Time Required: {self.time_required}, Dependencies: {self.dependencies}"

class Assembly(Part):
    def __init__(self, part_id, time_required, dependencies=[]):
        super().__init__(part_id, "MAKE", time_required, dependencies)

    def check_if_ready(self):
        self.is_ready = all(dep.is_ready for dep in self.dependencies)

class Station(simpy.Resource):
    def __init__(self, env, capacity=1):
        super().__init__(env, capacity)

class ManufacturingProcess:
    def __init__(self, env, mbom):
        self.env = env
        self.mbom = mbom  # This should be a structured representation of your MBOM

    def process_part(self, part):
        yield self.env.timeout(part.time_required)
        part.is_ready = True
        print(f"Part {part.part_id} processed at {self.env.now}")

def setup_simulation(env, mbom):
    manufacturing_process = ManufacturingProcess(env, mbom)
    for part in mbom:
        if not part.dependencies:  # Start with parts that have no dependencies
            env.process(manufacturing_process.process_part(part))

# Simulation setup
env = simpy.Environment()
mbom = [
    Part('P1', 'BUY', 2),
    Part('P2', 'BUY', 4),
    Assembly('A1', 5, dependencies=['P1', 'P2']),
]
setup_simulation(env, mbom)
env.run(until=100)