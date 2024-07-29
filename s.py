import simpy
import pandas as pd
import random
import plotly.express as px

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
            with station.operator_capacity.request() as request:
                yield request
                operation = yield station.operation_queue.get()
                yield self.env.timeout(operation['Hours'])
                self.log.append((self.operator_id, operation['Operation Title'], station.station_id, self.env.now))
                yield self.env.timeout(2)

# Define the Station class
class Station:
    def __init__(self, env, station_id):
        self.env = env
        self.station_id = station_id
        self.operators = []
        self.operation_queue = simpy.Store(env)
        self.operator_capacity = simpy.Resource(env, capacity=3)
        self.stand = None

    def accept_hull(self, hull):
        self.stand = hull
        operations = hull.get_station_operations()
        for _, operation in operations.iterrows():
            self.operation_queue.put(operation)

    def assign_operator(self, operator):
        if len(self.operators) < 3:
            self.operators.append(operator)
            operator.current_assignment = self
            return True
        return False

# Define the Line class
class Line:
    def __init__(self, env, floor_status, operation_data):
        self.env = env
        self.floor_status = floor_status
        self.operation_data = operation_data
        self.stations = {station: Station(env, station) for station in floor_status['Station']}
        self.initialize_hulls()

        # Simulation parameters
        self.head_count = 45
        self.operators = [Operator(env, f'Operator-{i}') for i in range(self.head_count)]
        self.rate = 1.25
        self.shift_duration = 8
        self.attrition_rates = {
            'Monday': (0.05, 0.15),
            'Tuesday': (0.05, 0.15),
            'Wednesday': (0.05, 0.15),
            'Thursday': (0.05, 0.15),
            'Friday': (0.05, 0.15),
            'Saturday': (0.00, 0.00),
            'Sunday': (0.00, 0.00)
        }
        self.efficiency = 0.7

    def initialize_hulls(self):
        for _, row in self.floor_status.iterrows():
            station = self.stations[row["Station"]]
            hull = Hull(self.env, row["Vin"], row["Program"], self.operation_data)
            hull.current_state = row["Station"]
            station.accept_hull(hull)

    def assign_operators(self):
        operator_index = 0
        for station_name, station in self.stations.items():
            if isinstance(station.stand, Hull):
                while len(station.operators) < 3 and operator_index < len(self.operators):
                    operator = self.operators[operator_index]
                    if station.assign_operator(operator):
                        self.env.process(operator.perform_operation(station))
                    operator_index += 1

    def run_line(self):
        while True:
            self.assign_operators()
            yield self.env.timeout(1)  # Check every hour

    def transition(self):
        while True:
            yield self.env.timeout(self.shift_duration / self.rate)
            for station_name, station in self.stations.items():
                if station.stand and isinstance(station.stand, Hull):
                    next_station_name = self.get_next_station(station_name)
                    if next_station_name:
                        next_station = self.stations[next_station_name]
                        if not next_station.stand:
                            hull = station.stand
                            station.stand = None
                            next_station.accept_hull(hull)
                            hull.move_to_next_state(next_station_name)
            self.assign_operators()

    def get_next_station(self, current_station):
        current_station_index = int(current_station.split()[-1])
        next_station_index = current_station_index + 1
        next_station = f'STA {next_station_index}'
        if next_station in self.stations:
            return next_station
        return None

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

# Initialize the simulation environment
env = simpy.Environment()

# Create the line and start the simulation
hull_assembly_line = Line(env, floor_status, operation_data)
env.process(hull_assembly_line.run_line())
env.process(hull_assembly_line.transition())

# Run the simulation for a week (5 days, 8 hours each day)
env.run(until=5 * 8)

# Gather logs
operation_logs = []
for operator in hull_assembly_line.operators:
    for log_entry in operator.log:
        operation_logs.append({
            'Operator': log_entry[0],
            'Operation': log_entry[1],
            'Station': log_entry[2],
            'End Time': log_entry[3]
        })

operation_df = pd.DataFrame(operation_logs)

# Calculate start times based on end times and durations
operation_df = operation_df.merge(operation_data[['Operation Title', 'Hours']], left_on='Operation', right_on='Operation Title')
operation_df['Start Time'] = operation_df['End Time'] - operation_df['Hours']

# Sort the operations by start time
operation_df = operation_df.sort_values(by='Start Time')

# Generate a Gantt chart using Plotly
fig = px.timeline(operation_df, x_start='Start Time', x_end='End Time', y='Station', color='Operator', title='Hull Assembly Line Operations')
fig.update_yaxes(categoryorder='category ascending')
fig.show()
