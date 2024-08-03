Limit Operators per Station:

Ensure each station only allows up to three operators at a time.
Single Operation per Operator:

Assign operators to a single operation at a time.
Hull Movement Only When Operations Complete:

Ensure hulls only move when all operations at the current station are complete.
Here's a detailed example of how you might adjust your code:

Adjust the Operator Class
Ensure that each operator performs only one operation at a time and request the station's operator capacity:

python
Copy code
class Operator:
    def __init__(self, env, operator_id):
        self.env = env
        self.operator_id = operator_id
        self.current_assignment = None

    def perform_operation(self, station):
        while True:
            if self.current_assignment is None:
                with station.operator_capacity.request() as request:
                    yield request
                    self.current_assignment = station

                    # Assign the operation
                    operation = yield station.operation_queue.get()
                    start_time = self.env.now
                    duration = operation.hours * random.uniform(0.5, 1.5) * station.efficiency
                    yield self.env.timeout(duration)
                    end_time = self.env.now

                    # Log the operation
                    operation_df.loc[len(operation_df)] = [self.operator_id, operation.name, station.station_id, self.current_assignment.hull.hull_id, start_time, end_time]
                    operation.complete()
                    self.current_assignment = None

                    # Release the operator from the station
                    yield self.env.timeout(0)
Adjust the Station Class
Ensure each station handles a maximum of three operators and tracks operations properly:

python
Copy code
class Station:
    def __init__(self, env, station_id, capacity=3):
        self.env = env
        self.station_id = station_id
        self.capacity = capacity
        self.operator_capacity = simpy.Resource(env, capacity)
        self.operation_queue = simpy.Store(env)
        self.current_operations = []

    def assign_operation(self, operation):
        self.operation_queue.put(operation)
        self.current_operations.append(operation)

    def all_operations_complete(self):
        return all(op.is_completed for op in self.current_operations)
Adjust the Hull Class
Ensure hulls only move when all operations at the current station are complete and handle movement between stations:

python
Copy code
class Hull:
    def __init__(self, env, hull_id, program, operation_data):
        self.env = env
        self.hull_id = hull_id
        self.program = program
        self.operation_data = operation_data
        self.current_state = None

    def move_to_next_state(self, next_state):
        if self.current_state and self.current_state.all_operations_complete():
            floor_status_df["Hull"].append(self.hull_id)
            floor_status_df["From"].append(self.current_state.station_id)
            floor_status_df["To"].append(next_state.station_id)
            floor_status_df["Time"].append(self.env.now)
            self.current_state = next_state

    def get_station_operations(self):
        return self.operation_data[self.operation_data["Program"] == self.program]
Adjust the Line Class
Ensure that the line handles hull transitions correctly and assigns operators appropriately:

python
Copy code
class Line:
    def __init__(self, env, floor_status, operation_data, available_hulls, downtime, attrition_rates, efficiency):
        self.env = env
        self.floor_status = floor_status
        self.operation_data = operation_data
        self.available_hulls = available_hulls
        self.downtime = downtime
        self.attrition_rates = attrition_rates
        self.efficiency = efficiency
        self.stations = {station_id: Station(env, station_id) for station_id in floor_status['Station']}
        self.operators = [Operator(env, f"Operator_{i}") for i in range(3 * len(self.stations))]

    def run_line(self):
        while True:
            for station in self.stations.values():
                if station.all_operations_complete():
                    next_station = self.get_next_station(station)
                    if next_station:
                        hull = station.current_operations.pop()
                        hull.move_to_next_state(next_station)
                        for operation in hull.get_station_operations():
                            next_station.assign_operation(operation)
            yield self.env.timeout(1)
Running the Simulation
Make sure the simulation runs properly and logs results as expected:

python
Copy code
env = simpy.Environment()
line = Line(env, floor_status_df, operation_df, available_hulls, downtime, attrition_rates, efficiency)
env.process(line.run_line())
env.run(until=100)

# Output the floor status log
floor_log_df = pd.DataFrame(line.floor_status, columns=["Time", "Status"])
print(floor_log_df)

# Output the operation log
operation_log_df = pd.DataFrame(operation_df)
print(operation_log_df)
