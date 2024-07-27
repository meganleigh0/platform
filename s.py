import simpy
import random

class Operation:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

class Station:
    def __init__(self, env, name, operations):
        self.env = env
        self.name = name
        self.operations = operations
        self.resource = simpy.Resource(env, capacity=3)  # Max 3 operators at a time
        self.operation_queue = simpy.Store(env)

    def add_operation(self, operation):
        self.operation_queue.put(operation)

class Operator:
    def __init__(self, env, name):
        self.env = env
        self.name = name

    def perform_operation(self, station):
        while True:
            with station.resource.request() as request:
                yield request
                operation = yield station.operation_queue.get()
                print(f'{self.name} starts {operation.name} at {station.name} at {self.env.now}')
                yield self.env.timeout(operation.duration)
                print(f'{self.name} completes {operation.name} at {station.name} at {self.env.now}')
            yield self.env.timeout(2 * 60)  # Reassign operators every 2 hours

def setup(env, num_operators, stations):
    operators = [Operator(env, f'Operator-{i}') for i in range(num_operators)]
    for operator in operators:
        for station in stations:
            env.process(operator.perform_operation(station))

# Initialize environment
env = simpy.Environment()

# Create operations
operations = [Operation(f'Operation-{i}', random.randint(10, 30)) for i in range(20)]

# Create stations and add operations to them
stations = [Station(env, f'Station-{i}', operations) for i in range(3)]
for station in stations:
    for operation in operations:
        station.add_operation(operation)

# Setup and run the simulation
setup(env, num_operators=9, stations=stations)
env.run(until=1000)

