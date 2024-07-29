import simpy
import pandas as pd
import plotly.express as px
import numpy as np

# Define the Hull class
class Hull:
    def __init__(self, env, hull_id, program, operation_data):
        self.env = env
        self.hull_id = hull_id
        self.program = program
        self.current_state = None
        self.log = []
        self.operation_data = operation_data

    def move_to_next_state(self, next_state):
        if self.current_state:
            self.log.append((self.hull_id, self.current_state, next_state, self.env.now))
            print(f"Hull {self.hull_id} moved from {self.current_state} to {next_state} at time {self.env.now}")
        self.current_state = next_state

    def get_station_operations(self):
        if self.operation_data is not None:
            return self.operation_data[self.operation_data['Station'] == self.current_state]
        return pd.DataFrame()

# Define the Operator class
class Operator:
    def __init__(self, env, operator_id):
        self.env = env
        self.operator_id = operator_id
        self.current_assignment = None
        self.log = []

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
                    self.log.append({
                        'Operator': self.operator_id,
                        'Operation': operation['Operation Title'],
                        'Station': station.station_id,
                        'Start Time': start_time,
                        'End Time': end_time
                    })
                    print(f"Operator {self.operator_id} performed {operation['Operation Title']} on {station.station_id} from {start_time} to {end_time}")
                    yield self.env.timeout(2)
            except simpy.Interrupt:
                break

# Define the Station class
class Station:
    def __init__(self, env, station_id):
        self.env = env
        self.station_id = station_id
        self.operators = []
        self.operation_queue = simpy.Store(env)
        self.operator_capacity = simpy.Resource(env, capacity=3)
        self.stand = None
        self.downtime = []

    def accept_hull(self, hull):
        self.stand = hull
        operations = hull.get_station_operations()
        for _, operation in operations.iterrows():
            self.operation_queue.put(operation)
        print(f"Hull {hull.hull_id} accepted at {self.station_id} with operations: {operations}")

    def assign_operator(self, operator):
        if len(self.operators) < self.operator_capacity.capacity and len(self.operators) < len(self.operation_queue.items) and not self.is_down():
            self.operators.append(operator)
            operator.current_assignment = self
            return True
        return False

    def is_down(self):
        for start_time, duration in self.downtime:
            if start_time <= self.env.now < start_time + duration:
                return True
        return False

    def add_downtime(self, start_time, duration):
        self.downtime.append((start_time, duration))

# Define the Line class
class Line:
    def __init__(self, env, floor_status, operation_data, available_hulls, downtime, attrition_rates, efficiency):
        self.env = env
        self.floor_status = floor_status
        self.operation_data = operation_data
        self.available_hulls = available_hulls
        self.attrition_rates = attrition_rates
        self.efficiency = efficiency
        self.stations = {station: Station(env, station) for station in floor_status['Station']}
        self.initialize_hulls()
        self.floor_log = []
        self.head_count = 45
        self.operators = [Operator(env, f'Operator-{i}') for i in range(self.head_count)]
        self.rate = 1.25
        self.shift_duration = 8
        self.completion_queue = []

        for station, (start_time, duration) in downtime.items():
            self.stations[station].add_downtime(start_time, duration)

    def initialize_hulls(self):
        for _, row in self.floor_status.iterrows():
            station = self.stations[row["Station"]]
            hull = Hull(self.env, row["Vin"], row["Program"], self.operation_data)
            hull.current_state = row["Station"]
            station.accept_hull(hull)

    def resample_headcount(self):
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][int(self.env.now // self.shift_duration) % 7]
        min_attrition, max_attrition = self.attrition_rates[day_of_week]
        attrition_rate = np.random.uniform(min_attrition, max_attrition)
        available_headcount = int(self.head_count * (1 - attrition_rate) * self.efficiency)
        self.operators = [Operator(self.env, f'Operator-{i}') for i in range(available_headcount)]
        print(f"Resampled headcount: {available_headcount} operators available on {day_of_week}")

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

    def run_line(self):
        while True:
            self.resample_headcount()
            self.assign_operators()
            self.log_floor_status()
            yield self.env.timeout(2)  # Assign operators every 2 hours
            self.attempt_transition()
            yield self.env.timeout(self.shift_duration / self.rate - 2)

    def attempt_transition(self):
        for station_name in sorted(self.stations.keys(), reverse=True):
            station = self.stations[station_name]
            if station.stand and isinstance(station.stand, Hull) and not station.is_down():
                if station.operation_queue.items:
                    continue  # Hull can't move if there are pending operations
                next_station_name = self.get_next_station(station_name)
                if next_station_name:
                    next_station = self.stations[next_station_name]
                    if not next_station.stand and not next_station.is_down():
                        hull = station.stand
                        station.stand = None
                        hull.move_to_next_state(next_station_name)
                        next_station.accept_hull(hull)
                        print(f"Hull {hull.hull_id} moved from {station_name} to {next_station_name} at time {self.env.now}")
                else:
                    # Place hull in completion queue if it's the final station
                    completed_hull = station.stand
                    station.stand = None
                    self.completion_queue.append(completed_hull)
                    print(f"Hull {completed_hull.hull_id} completed at {station_name} at time {self.env.now}")

            # Add available hull to the line if STA 0 is free
            if not self.stations['STA 0'].stand and self.available_hulls:
                new_hull_data = self.available_hulls.pop(0)
                new_hull = Hull(self.env, new_hull_data['HullID'], new_hull_data['Program'], self.operation_data)
                new_hull.current_state = 'STA 0'
                self.stations['STA 0'].accept_hull(new_hull)
                print(f"New hull {new_hull.hull_id} added to STA 0 at time {self.env.now}")


    def get_next_station(self, current_station):
        current_station_index = int(current_station.split()[-1])
        next_station_index = current_station_index + 1
        next_station = f'STA {next_station_index}'
        if next_station in self.stations:
            return next_station
        return None

    def log_floor_status(self):
        status = {station: (self.stations[station].stand.hull_id if self.stations[station].stand else None)
                  for station in self.stations}
        self.floor_log.append((self.env.now, status))
        print(f"Floor status at time {self.env.now}: {status}")

# Generate sample operation data
operation_data = pd.DataFrame({
    'Station': ['STA 0', 'STA 0', 'STA 1', 'STA 1', 'STA 2', 'STA 2', 'STA 3', 'STA 3', 'STA 4', 'STA 4', 'STA 5', 'STA 5'],
    'Operation Title': ['Op 0.1', 'Op 0.2', 'Op 1.1', 'Op 1.2', 'Op 2.1', 'Op 2.2', 'Op 3.1', 'Op 3.2', 'Op 4.1', 'Op 4.2', 'Op 5.1', 'Op 5.2'],
    'Hours': [1.0, 2.0, 1.5, 2.5, 2.0, 1.0, 3.0, 2.5, 2.0, 1.5, 1.0, 2.5]
})

# Define the initial floor status DataFrame
floor_status = pd.DataFrame({
    'Vin': ['TESTHull0', 'TESTHull1', 'TESTHull2', 'TESTHull3', 'TESTHull4', 'TESTHull5', 'TESTHull6', 'TESTHull7', 'TESTHull8'],
    'Station': ['STA 0', 'STA 1', 'STA 2', 'STA 3', 'STA 4', 'STA 5', 'STA 6', 'STA 7', 'STA 8'],
    'Program': ['SEPV3', 'SEPV3', 'SEPV3', 'SEPV3', 'SEPV3', 'SEPV3', 'SEPV3', 'SEPV3', 'SEPV3']
})

# Initialize available hulls and downtime
available_hulls = [{'HullID': 'Hull1', 'Program': 'SEPV3'}, {'HullID': 'Hull2', 'Program': 'SEPV3'}]
downtime = {'STA 0': (10, 2), 'STA 1': (20, 3)}

# Attrition rates and efficiency
attrition_rates = {
    'Monday': (0.05, 0.15),
    'Tuesday': (0.05, 0.15),
    'Wednesday': (0.05, 0.15),
    'Thursday': (0.05, 0.15),
    'Friday': (0.05, 0.15),
    'Saturday': (0.00, 0.00),
    'Sunday': (0.00, 0.00)
}
efficiency = 0.7

# Initialize the simulation environment
env = simpy.Environment()

# Create the line and start the simulation
hull_assembly_line = Line(env, floor_status, operation_data, available_hulls, downtime, attrition_rates, efficiency)
env.process(hull_assembly_line.run_line())

# Run the simulation for a week (5 days, 8 hours each day)
env.run(until=5 * 8)

# Gather logs
operation_logs = []
for operator in hull_assembly_line.operators:
    for log_entry in operator.log:
        operation_logs.append(log_entry)

# Convert operation logs to DataFrame
operation_df = pd.DataFrame(operation_logs)

# Check if the DataFrame is empty
if not operation_df.empty:
    # Ensure start times are correctly calculated
    operation_df = operation_df.rename(columns={'Operation': 'Operation Title'})
    operation_df = operation_df.merge(operation_data[['Operation Title', 'Hours']], on='Operation Title')
    operation_df['Start Time'] = operation_df['End Time'] - operation_df['Hours']

    # Sort the operations by start time
    operation_df = operation_df.sort_values(by='Start Time')

    # Generate a Gantt chart using Plotly
    fig = px.timeline(operation_df, x_start='Start Time', x_end='End Time', y='Station', color='Operator', title='Hull Assembly Line Operations')
    fig.update_yaxes(categoryorder='category ascending')
    fig.show()
else:
    print("No operation logs found.")

# Output the floor status log
floor_log_df = pd.DataFrame(hull_assembly_line.floor_log, columns=['Time', 'Status'])
print(floor_log_df)
