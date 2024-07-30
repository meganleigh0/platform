import pandas as pd
import simpy

# Initialize the DataFrame
operation_df = pd.DataFrame(columns=["OperatorID", "Operation", "Station", "HullID", "Start", "End"])

class Operator:
    def __init__(self, env, operator_id):
        self.env = env
        self.operator_id = operator_id
        self.current_assignment = None

    def perform_operation(self, station):
        self.current_assignment = station
        while True:
            try:
                with station.operator_capacity.request() as request:
                    yield request
                    operation = yield station.operation_queue.get()
                    start_time = self.env.now
                    yield self.env.timeout(operation['Hours'])
                    end_time = self.env.now

                    print(f"Operator {self.operator_id} performed operation {operation['Title']} from {station.station_id} from {start_time} to {end_time}")

                    # Append operation details to the DataFrame
                    hull = station.stand
                    operation_df.loc[len(operation_df)] = [self.operator_id, operation['Title'], station.station_id, hull.hull_id, start_time, end_time]

            except simpy.Interrupt:
                break

class Station:
    def __init__(self, env, station_id):
        self.env = env
        self.station_id = station_id
        self.operation_queue = simpy.Store(env)
        self.operator_capacity = simpy.Resource(env, capacity=3)
        self.downtime = []
        self.stand = None
        self.operators = []

    def accept_hull(self, hull):
        self.stand = hull
        operations = hull.get_station_operations()
        for operation in operations:
            self.operation_queue.put(operation)
        print(f"Hull {hull.hull_id} accepted at {self.station_id} with operations: {operations}")

    def is_down(self):
        for start_time, duration in self.downtime:
            if start_time <= self.env.now < start_time + duration:
                return True
        return False

    def add_downtime(self, start_time, duration):
        self.downtime.append((start_time, duration))

    def assign_operator(self, operator):
        if len(self.operators) < 3:
            self.operators.append(operator)
            return True
        return False

class Hull:
    def __init__(self, env, hull_id, program, operation_data):
        self.env = env
        self.hull_id = hull_id
        self.program = program
        self.current_state = None
        self.operation_data = operation_data

    def move_to_next_state(self, next_state):
        self.current_state = next_state

    def get_station_operations(self):
        if self.operation_data is not None:
            program_data = self.operation_data[self.operation_data["Program"] == self.program].copy()
            return program_data[program_data["Station"] == self.current_state].to_dict('records')
        return []

class Line:
    def __init__(self, env, floor_status, operation_data, available_hulls, downtime, attrition_rates, efficiency):
        self.env = env
        self.floor_status = floor_status
        self.operation_data = operation_data
        self.available_hulls = available_hulls
        self.attrition_rates = attrition_rates
        self.efficiency = efficiency
        self.stations = {station: Station(env, station) for station in floor_status['Station']}
        self.head_count = 45
        self.operators = [Operator(env, f"Operator_{i}") for i in range(self.head_count)]
        self.rate = 1.25
        self.shift_duration = 8 * 60  # 8 hours in minutes
        self.start_processes()

    def resample_headcount(self):
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][int(self.env.now // self.shift_duration) % 5]
        attrition_rate = self.attrition_rates[day_of_week]
        max_attrition = max(attrition_rate)
        new_headcount = int(self.head_count * (1 - max_attrition))
        self.operators = [Operator(self.env, f"Operator_{i}") for i in range(new_headcount)]
        print(f"Resampled headcount: {new_headcount} operators available on {day_of_week}")

    def start_processes(self):
        self.env.process(self.reassign_operators())
        self.env.process(self.attempt_transitions())
        self.env.process(self.resample_headcount_process())

    def reassign_operators(self):
        while True:
            self.assign_operators()
            self.log_floor_status()
            yield self.env.timeout(2 * 60)  # 2 hours

    def attempt_transitions(self):
        while True:
            yield self.env.timeout(8 * 60 / self.rate)  # 6.4 hours
            self.attempt_transition()
            self.log_floor_status()

    def resample_headcount_process(self):
        while True:
            yield self.env.timeout(8 * 60)  # 8 hours
            self.resample_headcount()
            self.log_floor_status()

    def assign_operators(self):
        operator_index = 0
        for station_name, station in self.stations.items():
            station.operators = []  # Clear current operators
            if isinstance(station.stand, Hull) and not station.is_down():
                num_operations = len(station.operation_queue.items)
                while len(station.operators) < min(3, num_operations) and operator_index < len(self.operators):
                    operator = self.operators[operator_index]
                    if station.assign_operator(operator):
                        self.env.process(operator.perform_operation(station))
                        operator_index += 1
                        print(f"Operator {operator.operator_id} assigned to {station_name}")

    def attempt_transition(self):
        for station_name in sorted(self.stations.keys(), reverse=True):
            station = self.stations[station_name]
            if isinstance(station.stand, Hull) and not station.is_down() and not station.operation_queue.items:
                next_station_name = self.get_next_station(station_name)
                if next_station_name:
                    next_station = self.stations[next_station_name]
                    if not next_station.stand and not next_station.is_down():
                        hull = station.stand
                        station.stand = None
                        hull.move_to_next_state(next_station_name)
                        next_station.accept_hull(hull)
                    else:
                        completed_hull = station.stand
                        station.stand = None
                        self.available_hulls.append(completed_hull)
                        print(f"Completed hull {completed_hull.hull_id} at {station_name} at time {self.env.now}")

    def get_next_station(self, current_station):
        current_index = int(current_station.split()[-1])
        next_index = current_index + 1
        next_station = f'STA {next_index}'
        if next_station in self.stations:
            return next_station
        return None

    def log_floor_status(self):
        for station_name, station in self.stations.items():
            if station.stand:
                status = station.stand.hull_id
            else:
                status = None
            print(f"Floor status at time {self.env.now}: {station_name} has hull {status}")

# Sample usage
env = simpy.Environment()

# Initialize floor_status, operation_data, available_hulls, downtime, attrition_rates, and efficiency
# These should be provided according to your dataset and requirements
floor_status = {
    'Station': ['STA 0', 'STA 1', 'STA 2', 'STA 3', 'STA 4']
}
operation_data = pd.DataFrame([
    {'Program': 'A', 'Station': 'STA 0', 'Operation': 'Op1', 'Hours': 2},
    {'Program': 'A', 'Station': 'STA 1', 'Operation': 'Op2', 'Hours': 3},
    {'Program': 'A', 'Station': 'STA 2', 'Operation': 'Op3', 'Hours': 4},
    {'Program': 'A', 'Station': 'STA 3', 'Operation': 'Op4', 'Hours': 5},
    {'Program': 'A', 'Station': 'STA 4', 'Operation': 'Op5', 'Hours': 6}
])
available_hulls = [Hull(env, f'Hull_{i}', 'A', operation_data) for i in range(5)]
downtime = {}
attrition_rates = {
    'Monday': [0.0, 0.1],
    'Tuesday': [0.0, 0.1],
    'Wednesday': [0.0, 0.1],
    'Thursday': [0.0, 0.1],
    'Friday': [0.0, 0.1]
}
efficiency = 1.0

line = Line(env, floor_status, operation_data, available_hulls, downtime, attrition_rates, efficiency)

# Add an initial hull to the first station for testing
env.process(line.stations['STA 0'].accept_hull(available_hulls.pop(0)))

# Run the simulation for a specific period (e.g., 48 hours)
env.run(until=48 * 60)

print(operation_df)