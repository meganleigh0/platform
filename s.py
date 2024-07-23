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

# Operation Data
operation_data = pd.concat([
    pd.DataFrame({
        'Station': ['STA 0', 'STA 0', 'STA 1', 'STA 1', 'STA 2'],
        'Operation': ['Build', 'Assemble', 'Tear', 'Dry', 'Paint'],
        'Program': ['A', 'A', 'A', 'A', 'A'],
        'Hours': [0.23, 0.3, 0.5, 1.0, 3.0]
    }),
    pd.DataFrame({
        'Station': ['STA 0', 'STA 0', 'STA 1', 'STA 1', 'STA 2'],
        'Operation': ['Build', 'Assemble', 'Tear', 'Dry', 'Paint'],
        'Program': ['B', 'B', 'B', 'B', 'B'],
        'Hours': [0.25, 0.35, 0.55, 1.1, 3.2]
    })
])

# Available Hulls
available_hulls = {
    'A': 5,
    'B': 3
}

# Initial Floor Status
floor_status = pd.DataFrame({
    'Vin': ['Hull 1', 'Hull 2', 'Hull 3'],
    'Station': ['STA 0', 'STA 1', 'STA 2'],
    'Program': ['A', 'A', 'A']
})

# Downtime
downtime = {
    'STA 1': (4, 2)  # Station STA 1 is down from hour 4 to hour 6
}

# Outputs
operation_log = []
line_moves = []
daily_operator_requirements = []
hulls_processed = []
attrition_log = []

class Station:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.resource = simpy.Resource(env, capacity=1)

def calculate_attrition(day):
    rate_range = attrition_rates[day]
    return random.uniform(*rate_range)

def operator_allocation(env, operators_needed, available_employees):
    operators_assigned = min(operators_needed, available_employees[0])
    if operators_assigned > 0:
        available_employees[0] -= operators_assigned
        yield env.timeout(shift_duration / operators_assigned)
        available_employees[0] += operators_assigned
    else:
        yield env.timeout(shift_duration)

def process_hull(env, hull, stations, available_employees):
    while True:
        current_station = hull['Station']
        if current_station == 'COMPLETED':
            break
        station = stations[current_station]

        with station.resource.request() as request:
            yield request

            operations = operation_data[(operation_data['Station'] == current_station) & (operation_data['Program'] == hull['Program'])]
            for i, (index, operation) in enumerate(operations.iterrows()):
                actual_time = operation['Hours'] * random.uniform(0.5, 1.5) * efficiency
                yield env.timeout(actual_time)
                start_time = env.now - actual_time
                end_time = env.now
                operation_log.append((operation['Operation'], start_time, end_time, current_station, hull['Vin']))

            current_station_index = int(current_station.split(' ')[1])
            if current_station_index < 2:
                next_station = 'STA ' + str(current_station_index + 1)
            else:
                next_station = 'COMPLETED'
                hulls_processed.append(hull['Vin'])

            hull['Station'] = next_station
            line_moves.append((env.now, hull['Vin'], current_station, next_station))

def run_simulation(env, run_time, employee_count, start_date, daily_hull_rate):
    global floor_status
    available_employees = [employee_count]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    stations = {f'STA {i}': Station(env, f'STA {i}') for i in range(3)}  # Adjust range as needed
    
    for day in range(run_time):
        current_day = days[day % len(days)]
        attrition = calculate_attrition(current_day)
        available_employees[0] -= int(available_employees[0] * attrition)
        
        attrition_log.append({
            'Day': day + 1,
            'Available Employees': available_employees[0]
        })

        for index, row in floor_status.iterrows():
            env.process(process_hull(env, row, stations, available_employees))
        
        hulls_processed_today = 0
        while hulls_processed_today < daily_hull_rate:
            hulls_processed_today += 1
            env.run(until=env.now + shift_duration / daily_hull_rate)
        
        daily_operator_requirements.append({
            'Day': day + 1,
            'Available Employees': available_employees[0]
        })

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
operation_df = pd.DataFrame(operation_log, columns=['Operation', 'Start Time', 'End Time', 'Station', 'Vehicle'])
line_moves_df = pd.DataFrame(line_moves, columns=['Time', 'Vehicle', 'From Station', 'To Station'])
daily_operator_requirements_df = pd.DataFrame(daily_operator_requirements)
attrition_log_df = pd.DataFrame(attrition_log)

print(operation_df)
print(line_moves_df)
print(daily_operator_requirements_df)
print(attrition_log_df)
