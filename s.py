import simpy
import random
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Define classes for Hull, Station, Operator, Scheduler, and DataCollector

class Hull:
    def __init__(self, hull_id, program):
        self.id = hull_id
        self.program = program
        self.current_station = None
        self.start_time = None
        self.end_time = None

    def move_to_next_station(self, next_station):
        self.current_station = next_station

class Station:
    def __init__(self, station_id):
        self.id = station_id
        self.capacity = 1
        self.operations = []
        self.current_hull = None
        self.downtime_schedule = []

    def is_available(self, current_time):
        return self.current_hull is None and all(downtime[0] > current_time or downtime[1] < current_time for downtime in self.downtime_schedule)

    def schedule_downtime(self, start, duration):
        self.downtime_schedule.append((start, start + duration))
    
    def process_hull(self, hull, operation_time):
        self.current_hull = hull
        return operation_time

class Operator:
    def __init__(self, operator_id):
        self.id = operator_id
        self.station = None
        self.shift_schedule = []

    def assign_to_station(self, station, start_time, end_time):
        self.station = station
        self.shift_schedule.append((start_time, end_time))

    def is_available(self, current_time):
        return all(start > current_time or end < current_time for start, end in self.shift_schedule)

class Scheduler:
    def __init__(self, operators, stations, attrition_rate):
        self.operators = operators
        self.stations = stations
        self.attrition_rate = attrition_rate

    def assign_operators(self, current_time):
        for operator in self.operators:
            if operator.is_available(current_time):
                available_stations = [station for station in self.stations if station.is_available(current_time)]
                if available_stations:
                    station = random.choice(available_stations)  # Random selection logic
                    operator.assign_to_station(station, current_time, current_time + 2)
                    station.current_hull = None  # Assuming operator assignment frees the station

    def schedule_line_movements(self, current_time):
        for station in self.stations:
            if station.current_hull:
                next_station = self.get_next_station(station.id)
                if next_station and next_station.is_available(current_time):
                    next_station.current_hull = station.current_hull
                    station.current_hull = None

    def handle_attrition(self):
        for operator in self.operators:
            if random.random() < self.attrition_rate:
                operator.station = None
                operator.shift_schedule = []

    def get_next_station(self, current_station_id):
        next_station_id = (current_station_id + 1) % len(self.stations)
        return self.stations[next_station_id]

class DataCollector:
    def __init__(self):
        self.operation_table = []
        self.floor_status = []
        self.line_movement_log = []

    def record_operation(self, hull, station, start_time, end_time, operator_id):
        self.operation_table.append({
            'hull_id': hull.id,
            'station_id': station.id,
            'start_time': start_time,
            'end_time': end_time,
            'operator_id': operator_id
        })

    def record_floor_status(self, current_time, stations):
        status = {station.id: (station.current_hull.id if station.current_hull else None) for station in stations}
        self.floor_status.append({
            'time': current_time,
            'status': status
        })

    def record_line_movement(self, time, hull_id, from_station, to_station):
        self.line_movement_log.append({
            'time': time,
            'hull_id': hull_id,
            'from_station': from_station,
            'to_station': to_station
        })

# Define the simulation functions

def hull_lifecycle(env, hull, stations, scheduler, data_collector):
    for station in stations:
        while not station.is_available(env.now):
            yield env.timeout(1)
        operation_time = station.process_hull(hull, 2)
        start_time = env.now
        yield env.timeout(operation_time)
        end_time = env.now
        data_collector.record_operation(hull, station, start_time, end_time, None)  # Operator ID logic needed
        hull.move_to_next_station(station)
        next_station = scheduler.get_next_station(station.id)
        data_collector.record_line_movement(env.now, hull.id, station.id, next_station.id)
        station.current_hull = None

def operator_lifecycle(env, scheduler):
    while True:
        scheduler.assign_operators(env.now)
        scheduler.schedule_line_movements(env.now)
        scheduler.handle_attrition()
        yield env.timeout(2)

def initialize_simulation(env, num_hulls, daily_hull_rate, operators, stations, scheduler, data_collector, start_day, run_time):
    hulls = [Hull(f'Hull{i+1}', random.choice(['A', 'B', 'C'])) for i in range(num_hulls)]
    for hull in hulls:
        hull.start_time = env.now
        env.process(hull_lifecycle(env, hull, stations, scheduler, data_collector))

    current_date = datetime.now()
    start_date = current_date + timedelta(days=start_day)
    end_date = start_date + timedelta(days=run_time)

    while current_date < end_date:
        for _ in range(int(daily_hull_rate * 8)):
            if hulls:
                hull = hulls.pop(0)
                env.process(hull_lifecycle(env, hull, stations, scheduler, data_collector))
        env.run(until=env.now + 8)
        current_date += timedelta(days=1)

def run_simulation(headcount, start_day, shifts, operation_data, available_hulls, employee_count, start_date, run_time, floor_status, downtime, production_rate):
    env = simpy.Environment()
    operators = [Operator(i) for i in range(employee_count)]
    stations = [Station(i) for i in range(17)]
    scheduler = Scheduler(operators, stations, attrition_rate=0.05)
    data_collector = DataCollector()

    # Map station names to indices
    station_name_to_index = {f'STA {i}': i for i in range(17)}

    for station_name, dt in downtime.items():
        station_index = station_name_to_index[station_name]
        stations[station_index].schedule_downtime(dt[0], dt[1])

    initialize_simulation(env, len(available_hulls), production_rate, operators, stations, scheduler, data_collector, start_day, run_time)
    env.process(operator_lifecycle(env, scheduler))
    env.run(until=run_time * 24 * 60)  # Run for the given number of days

    # Convert collected data to pandas DataFrames and output results
    operation_table_df = pd.DataFrame(data_collector.operation_table)
    floor_status_df = pd.DataFrame(data_collector.floor_status)
    line_movement_log_df = pd.DataFrame(data_collector.line_movement_log)

    # Output the results
    print("Operation Table:")
    print(operation_table_df)
    print("\nFloor Status:")
    print(floor_status_df)
    print("\nLine Movement Log:")
    print(line_movement_log_df)
    
    return operation_table_df

# Sample data for the simulation
headcount = 50
start_day = 0  # Monday
shifts = 1
operation_data = [
    {'station': 0, 'operation': 'Build', 'hours': 0.23, 'program': 'A'},
    {'station': 0, 'operation': 'Assemble', 'hours': 1.3, 'program': 'B'},
    {'station': 0, 'operation': 'Assemble', 'hours': 0.3, 'program': 'B'},
    {'station': 1, 'operation': 'Tear', 'hours': 0.5, 'program': 'A'},
    {'station': 1, 'operation': 'Dry', 'hours': 1, 'program': 'A'},
    {'station': 2, 'operation': 'Paint', 'hours': 3, 'program': 'A'},
]
available_hulls = [
    {'HulID': 'Hull1', 'Program': 'A'},
    {'HulID': 'Hull2', 'Program': 'B'},
    {'HulID': 'Hull3', 'Program': 'C'},
]
employee_count = 10
start_date = datetime.now()
run_time = 5  # Run the simulation for 5 days
floor_status = [
    {'station': 0, 'hull_id': 'Hull1', 'program': 'A'},
    {'station': 1, 'hull_id': 'Hull2', 'program': 'B'},
    {'station': 2, 'hull_id': None, 'program': None},
]
downtime = {'STA 0': (10, 2)}
production_rate = 1.25

operation_table_df = run_simulation(headcount, start_day, shifts, operation_data, available_hulls, employee_count, start_date, run_time, floor_status, downtime, production_rate)

# Plotting the Gantt chart
df = operation_table_df.copy()

# Convert the time columns to float if they are not already
df['start_time'] = df['start_time'].astype(float)
df['end_time'] = df['end_time'].astype(float)

# Convert the time to a proper timedelta format
df['start_time'] = pd.to_timedelta(df['start_time'], unit='h')
df['end_time'] = pd.to_timedelta(df['end_time'], unit='h')

# For plotting, we need a reference date, assuming all times are relative to the same day
reference_date = pd.Timestamp('2024-07-01')
df['start_time'] = reference_date + df['start_time']
df['end_time'] = reference_date + df['end_time']

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="start_time", x_end="end_time", y="station_id", color="hull_id", title='Operation Timeline')

fig.show()
