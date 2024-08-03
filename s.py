   def start_operators(self):
        # Start the operators' tasks in parallel
        for operator, station in self.assigned_operators:
            self.env.process(self.perform_operation(operator, station))

    def perform_operation(self, operator, station):
        # Operator performs operations from the station's queue
        while True:
            if len(station.operation_queue.items) == 0:
                break
            operation = yield station.operation_queue.get()
            print(f"{operator} at {station.name} is performing operation taking {operation.time} time units at time {self.env.now}.")
            yield self.env.timeout(operation.time)
import simpy

class Line:
    def __init__(self, env, total_operators):
        self.env = env
        self.stations = {}  # Dictionary of station_name: station
        self.total_operators = total_operators
        self.operators = [f"Operator_{i}" for i in range(1, total_operators + 1)]
        self.assigned_operators = []
        self.shift_end_event = simpy.Event(env)  # Event to signal the end of the shift

    def assign_operators(self):
        while True:
            # Assign operators at the beginning of the shift
            self.assign_shift_operators()
            # Start all assigned operators in parallel
            self.start_operators()
            # Wait for 8 hours (shift duration)
            yield self.env.timeout(8)
            # Signal the end of the shift
            self.shift_end_event.succeed()
            # Wait a short time to ensure all operators stop
            yield self.env.timeout(1)
            # Reset the shift end event for the next shift
            self.shift_end_event = simpy.Event(self.env)
            # Release operators at the end of the shift
            self.release_operators()

    def assign_shift_operators(self):
        # Filter out stations without a Hull in the stand or with no operations
        eligible_stations = [s for s in self.stations.values() if isinstance(s.stand, Hull) and len(s.operation_queue.items) > 0]

        # Sort stations by the size of the operation queue and total processing time in descending order
        sorted_stations = sorted(
            eligible_stations,
            key=lambda s: (len(s.operation_queue.items), sum(op.time for op in s.operation_queue.items)),
            reverse=True
        )

        # Step 1: Ensure every station with a Hull has at least one operator
        for station in sorted_stations:
            if len(station.operators) == 0 and self.operators:
                operator = self.operators.pop(0)
                station.operators.append(operator)
                self.assigned_operators.append((operator, station))
                print(f"Assigned operator {operator} to station {station.name}")

        # Step 2: Distribute remaining operators up to the capacity of each station based on priority
        while self.operators:
            for station in sorted_stations:
                if self.operators and len(station.operators) < station.operator_capacity.capacity:
                    operator = self.operators.pop(0)
                    station.operators.append(operator)
                    self.assigned_operators.append((operator, station))
                    print(f"Assigned operator {operator} to station {station.name}")

    def start_operators(self):
        # Start the operators' tasks in parallel
        for operator, station in self.assigned_operators:
            self.env.process(self.perform_operation(operator, station))

    def perform_operation(self, operator, station):
        while True:
            if len(station.operation_queue.items) == 0 or self.shift_end_event.triggered:
                break
            operation = yield station.operation_queue.get()
            print(f"{operator} at {station.name} is performing operation taking {operation.time} time units.")
            yield self.env.timeout(operation.time)

    def release_operators(self):
        # Release all assigned operators
        for operator, station in self.assigned_operators:
            station.operators.remove(operator)
            self.operators.append(operator)
            print(f"Released operator {operator} from station {station.name}")
        self.assigned_operators.clear()

class Station:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.operators = []
        self.stand = None  # Initially, no Hull in the stand
        self.operator_capacity = simpy.Resource(env, capacity=3)
        self.operation_queue = simpy.Store(env)  # Use SimPy Store for operation queue

class Hull:
    def __init__(self, id):
        self.id = id

class Operation:
    def __init__(self, time):
        self.time = time

# Example usage
env = simpy.Environment()
line = Line(env, total_operators=10)  # Assume we have a total of 10 operators

# Create some stations and add them to the line
station1 = Station(env, "Station1")
station2 = Station(env, "Station2")
station3 = Station(env, "Station3")

# Add operations to the queues
station1.operation_queue.items.extend([Operation(5), Operation(3)])
station2.operation_queue.items.extend([Operation(7)])
station3.operation_queue.items.extend([Operation(6), Operation(4), Operation(2)])

line.stations["Station1"] = station1
line.stations["Station2"] = station2
line.stations["Station3"] = station3

# Put a Hull in the stand of station1 and station2
station1.stand = Hull(1)
station2.stand = Hull(2)

# Run the assign_operators process
env.process(line.assign_operators())
env.run(until=24)  # Run the simulation for 24 hours

# Output the operator assignments after simulation
for station_name, station in line.stations.items():
    print(f"{station_name} operators: {station.operators}")