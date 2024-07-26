import simpy
import pandas as pd
import random
import numpy as np

# Simulation Parameters
attrition_rates = {
    'Monday': (0.05, 0.15),
    'Tuesday': (0.05, 0.15),
    'Wednesday': (0.05, 0.15),
    'Thursday': (0.05, 0.15),
    'Friday': (0.25, 0.35)
}
shift_duration = 8  # hours
daily_hull_rate = 1.25
efficiency = 0.7  # Average efficiency
block_duration = 2  # hours

# Operation Data
operation_data = pd.concat([
    pd.DataFrame({
        'Station': [f'STA {i}' for i in range(17)],
        'Operation': [f'Build_{i}' for i in range(17)],
        'Program': ['A'] * 17,
        'Hours': [0.23, 0.3, 0.5, 1.0, 3.0, 0.25, 0.35, 0.55, 1.1, 3.2, 0.25, 0.35, 0.55, 1.1, 3.2, 0.23, 0.3]
    }),
    pd.DataFrame({
        'Station': [f'STA {i}' for i in range(17)],
        'Operation': [f'Build_{i}' for i in range(17)],
        'Program': ['B'] * 17,
        'Hours': [0.25, 0.35, 0.55, 1.1, 3.2, 0.25, 0.35, 0.55, 1.1, 3.2, 0.25, 0.35, 0.55, 1.1, 3.2, 0.23, 0.3]
    })
])

# Available Hulls
available_hulls = {
    'A': 5,
    'B': 3
}

# Initial Floor Status
floor_status = pd.DataFrame({
    'Vin': [f'TESTHull{i}' for i in range(1, 18)],
    'Station': [f'STA {i}' for i in range(17)],
    'Program': ['A'] * 17
})

# Downtime
downtime = {
    'STA 1': (4, 2)  # Station STA 1 is down from hour 4 to hour 6
}

# Outputs
operation_log = []
line_moves = []
operator_assignment_log = []
attrition_log = []
hulls_processed = []

class Station:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.capacity = simpy.Resource(env, capacity=1)  # Only one hull at a time
        self.operator_capacity = simpy.Resource(env, capacity=3)  # Up to 3 operators
        self.downtime = False
        self.downtime_start = 0
        self.downtime_duration = 0

    def set_downtime(self, start, duration):
        self.downtime = True
        self.downtime_start = start
        self.downtime_duration = duration

    def clear_downtime(self):
        self.downtime = False
        self.downtime_start = 0
        self.downtime_duration = 0

def calculate_attrition(day):
    rate_range = attrition_rates[day]
    return random.uniform(*rate_range)

def operator_allocation(env, station, operation, hull, operator):
    with station.operator_capacity.request() as request:
        yield request
        start_time = env.now
        actual_time = operation['Hours'] * random.uniform(0.5, 1.5) * efficiency
        yield env.timeout(actual_time)
        end_time = env.now
        operation_log.append((operation['Operation'], start_time, end_time, operator, station.name, hull['Vin']))
        operator_assignment_log.append((operator, station.name, start_time, end_time))

def process_hull(env, hull, stations, operators):
    while True:
        current_station = hull['Station']
        if current_station == 'COMPLETED':
            break
        station = stations[current_station]

        # Handle downtime
        if station.downtime and station.downtime_start <= env.now < station.downtime_start + station.downtime_duration:
            yield env.timeout(station.downtime_duration - (env.now - station.downtime_start))
            station.clear_downtime()

        with station.capacity.request() as request:
            yield request
            operations = operation_data[(operation_data['Station'] == current_station) & (operation_data['Program'] == hull['Program'])]
            parallel_tasks = [env.process(operator_allocation(env, station, operation, hull, operator)) for operator, (_, operation) in zip(operators, operations.iterrows())]
            yield simpy.events.AllOf(env, parallel_tasks)

            current_station_index = int(current_station.split(' ')[1])
            if current_station_index < 16:
                next_station = f'STA {current_station_index + 1}'
                if not stations[next_station].capacity.users:
                    hull['Station'] = next_station
                    line_moves.append((env.now, hull['Vin'], current_station, next_station))
            else:
                hull['Station'] = 'COMPLETED'
                hulls_processed.append(hull['Vin'])

def run_simulation(env, run_time, employee_count, start_date, daily_hull_rate):
    global floor_status
    available_employees = [employee_count]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    stations = {f'STA {i}': Station(env, f'STA {i}') for i in range(17)}  # Adjust range as needed
    
    operators = [f'Operator {i}' for i in range(employee_count)]

    # Set station downtimes
    for station_id, (start, duration) in downtime.items():
        stations[station_id].set_downtime(start, duration)

    for day in range(run_time):
        current_day = days[day % len(days)]
        attrition = calculate_attrition(current_day)
        available_employees[0] -= int(available_employees[0] * attrition)
        
        attrition_log.append({
            'Day': day + 1,
            'Available Employees': available_employees[0]
        })

        for index, row in floor_status.iterrows():
            env.process(process_hull(env, row, stations, operators))
        
        num_cycles = int(24 / (daily_hull_rate / 8))
        for _ in range(num_cycles):
            env.run(until=env.now + (8 / daily_hull_rate))

            # Check if all hulls at current stations are complete and move to the next station
            for index, hull in floor_status.iterrows():
                current_station = hull['Station']
                if current_station != 'COMPLETED':
                    current_station_index = int(current_station.split(' ')[1])
                    next_station = f'STA {current_station_index + 1}'
                    if current_station_index < 16 and not stations[next_station].capacity.users:
                        floor_status.at[index, 'Station'] = next_station
                        line_moves.append((env.now, hull['Vin'], current_station, next_station))

            # Pull a new hull onto the line at station 0 if available
            for program, qty in available_hulls.items():
                if qty > 0:
                    if len(floor_status[(floor_status['Station'] == 'STA 0') & (floor_status['Program'] == program)]) < 1:
                        new_hull_vin = f'HULL{len(floor_status) + 1}'
                        new_hull = pd.DataFrame({'Vin': [new_hull_vin], 'Station': ['STA 0'], 'Program': [program]})
                        floor_status = pd.concat([floor_status, new_hull], ignore_index=True)
                        available_hulls[program] -= 1

        available_employees[0] = employee_count

# Define scenario parameters
employee_count = 15
start_date = 'Monday'
run_time = 10

# Initialize the simulation environment
env = simpy.Environment()

# Run the simulation
run_simulation(env, run_time, employee_count, start_date, daily_hull_rate)

# Output results
operation_df = pd.DataFrame(operation_log, columns=['Operation', 'Start Time', 'End Time', 'Operator', 'Station', 'Vehicle'])
line_moves_df = pd.DataFrame(line_moves, columns=['Time', 'Vehicle', 'From Station', 'To Station'])
attrition_log_df = pd.DataFrame(attrition_log)
operator_assignment_df = pd.DataFrame(operator_assignment_log, columns=['OperatorID', 'Station', 'Start Time', 'End Time'])

import ace_tools as tools; tools.display_dataframe_to_user(name="Operation Log", dataframe=operation_df)
tools.display_dataframe_to_user(name="Line Moves", dataframe=line_moves_df)
tools.display_dataframe_to_user(name="Attrition Log", dataframe=attrition_log_df)
tools.display_dataframe_to_user(name="Operator Assignment Log", dataframe=operator_assignment_df)
