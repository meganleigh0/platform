import simpy
import pandas as pd
import random
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

def calculate_attrition(day):
    rate_range = attrition_rates[day]
    return random.uniform(*rate_range)

def downtime_propagation(station_name, env, downtime, station_processes, available_employees):
    start_time, duration = downtime[station_name]
    yield env.timeout(start_time)
    station_processes[station_name].interrupt('downtime')
    yield env.timeout(duration)
    station_processes[station_name] = env.process(station_process(env, station_name, available_employees, station_processes))

def operator_allocation(env, station_name, operators_needed, max_operators, available_employees):
    operators_assigned = min(operators_needed, max_operators, available_employees[0])
    if operators_assigned > 0:
        available_employees[0] -= operators_assigned
        yield env.timeout(shift_duration / operators_assigned)
        available_employees[0] += operators_assigned
    else:
        yield env.timeout(shift_duration)

def station_process(env, station_name, available_employees, station_processes):
    try:
        while True:
            current_hull = None
            for index, row in floor_status.iterrows():
                if row['Station'] == station_name:
                    current_hull = row
                    break

            if current_hull is not None:
                operations = operation_data[(operation_data['Station'] == station_name) & (operation_data['Program'] == current_hull['Program'])]
                parallel_tasks = [env.process(operator_allocation(env, station_name, 1, 3, available_employees)) for _ in range(len(operations))]
                results = yield simpy.events.AllOf(env, parallel_tasks)
                
                for i, (index, operation) in enumerate(operations.iterrows()):
                    start_time = env.now - shift_duration / len(operations) * (len(operations) - i)
                    actual_time = operation['Hours'] * random.uniform(0.5, 1.5) * efficiency
                    end_time = env.now + actual_time
                    operation_log.append((operation['Operation'], start_time, end_time, station_name, current_hull['Vin']))
                
                current_station_index = int(station_name.split(' ')[1])
                if current_station_index < 2:
                    next_station = 'STA ' + str(current_station_index + 1)
                else:
                    next_station = 'COMPLETED'
                    hulls_processed.append(current_hull['Vin'])
                floor_status.loc[floor_status['Vin'] == current_hull['Vin'], 'Station'] = next_station
                line_moves.append((env.now, current_hull['Vin'], station_name, next_station))
                
                if downtime.get(station_name):
                    yield env.process(downtime_propagation(station_name, env, downtime, station_processes, available_employees))
            else:
                yield env.timeout(1)
    except simpy.Interrupt as interrupt:
        if interrupt.cause == 'downtime':
            yield env.timeout(downtime[station_name][1])

def run_simulation(env, run_time, employee_count, start_date, daily_hull_rate):
    global floor_status
    available_employees = [employee_count]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    for day in range(run_time):
        current_day = days[day % len(days)]
        attrition = calculate_attrition(current_day)
        available_employees[0] -= int(available_employees[0] * attrition)
        
        attrition_log.append({
            'Day': day + 1,
            'Available Employees': available_employees[0]
        })

        # Initialize processes for each station
        station_processes = {}
        for station_name in operation_data['Station'].unique():
            station_processes[station_name] = env.process(station_process(env, station_name, available_employees, station_processes))

        # Ensure rate of hulls is met
        hulls_processed_today = 0
        while hulls_processed_today < daily_hull_rate:
            hulls_processed_today += 1
            env.run(until=env.now + shift_duration / daily_hull_rate)
        
        # Track daily operator requirements
        daily_operator_requirements.append({
            'Day': day + 1,
            'Available Employees': available_employees[0]
        })

        # Pull new hulls into STA 0 if available
        for program, qty in available_hulls.items():
            if qty > 0:
                if len(floor_status[(floor_status['Station'] == 'STA 0') & (floor_status['Program'] == program)]) < 1:
                    new_hull_vin = f'HULL{len(floor_status) + 1}'
                    new_hull = pd.DataFrame({'Vin': [new_hull_vin], 'Station': ['STA 0'], 'Program': [program]})
                    floor_status = pd.concat([floor_status, new_hull], ignore_index=True)
                    available_hulls[program] -= 1

        # Restore employees for the next day
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

def analyze_efficiency(operation_df, line_moves_df, employee_count, shift_duration):
    # Calculate total hours spent at each station
    station_hours = operation_df.groupby('Station')['End Time'].sum() - operation_df.groupby('Station')['Start Time'].sum()

    # Calculate the number of vehicles processed by each station
    vehicles_processed = line_moves_df.groupby('From Station')['Vehicle'].nunique()

    # Calculate HPU per station
    hpu_per_station = station_hours / vehicles_processed

    # Calculate overall HPU
    total_hours = operation_df['End Time'].sum() - operation_df['Start Time'].sum()
    total_vehicles = line_moves_df['Vehicle'].nunique()
    overall_hpu = total_hours / total_vehicles

    # Determine optimal operator assignment and shifts
    station_efficiency = {}
    for station in station_hours.index:
        hours = station_hours[station]
        vehicles = vehicles_processed[station]
        hpu = hpu_per_station[station]
        daily_hours_needed = hours / run_time
        recommended_operators = min(3, max(1, int(daily_hours_needed / shift_duration)))
        recommended_shifts = min(2, max(1, daily_hours_needed / (recommended_operators * shift_duration)))  # Cap shifts at 2
        station_efficiency[station] = {
            'Total Hours': hours,
            'Vehicles Processed': vehicles,
            'HPU': hpu,
            'Daily Hours Needed': daily_hours_needed,
            'Recommended Operators': recommended_operators,
            'Recommended Shifts': recommended_shifts
        }

    return station_efficiency, overall_hpu

# Perform the analysis
station_efficiency, overall_hpu = analyze_efficiency(operation_df, line_moves_df, employee_count, shift_duration)

# Output the analysis results
station_efficiency_df = pd.DataFrame(station_efficiency).T
print(station_efficiency_df)
print(f"Overall HPU: {overall_hpu:.2f}")

def suggest_operator_assignments(station_efficiency, available_employees, run_time):
    assignments = []
    remaining_employees = available_employees
    for day in range(run_time):
        daily_assignments = []
        for station, info in station_efficiency.items():
            operators = min(info['Recommended Operators'], remaining_employees)
            shifts = min(2, info['Recommended Shifts'])  # Cap shifts at 2
            daily_assignments.append({
                'Day': day + 1,
                'Station': station,
                'Assigned Operators': operators,
                'Assigned Shifts': shifts
            })
            remaining_employees -= operators

        assignments.extend(daily_assignments)
        remaining_employees = available_employees

    return pd.DataFrame(assignments)

# Suggest operator assignments
assignments_df = suggest_operator_assignments(station_efficiency, employee_count, run_time)
print(assignments_df)

def weekly_shift_plan(assignments_df, shift_duration):
    total_shifts = assignments_df['Assigned Shifts'].sum()
    total_hours_needed = total_shifts * shift_duration
    weeks_needed = total_hours_needed / (assignments_df['Day'].max() * shift_duration)
    return weeks_needed

weeks_needed = weekly_shift_plan(assignments_df, shift_duration)
print(f"Estimated Weeks Needed to Complete Production: {weeks_needed:.2f}")

def rebalance_for_downtime(station_name, day, downtime_duration, station_efficiency, available_employees):
    for station, info in station_efficiency.items():
        if station == station_name:
            daily_hours_needed = info['Daily Hours Needed'] + downtime_duration
            recommended_operators = min(3, max(1, int(daily_hours_needed / shift_duration)))
            recommended_shifts = min(2, max(1, daily_hours_needed / (recommended_operators * shift_duration)))  # Cap shifts at 2
            station_efficiency[station] = {
                'Total Hours': info['Total Hours'],
                'Vehicles Processed': info['Vehicles Processed'],
                'HPU': info['HPU'],
                'Daily Hours Needed': daily_hours_needed,
                'Recommended Operators': recommended_operators,
                'Recommended Shifts': recommended_shifts
            }
    return station_efficiency

# Example of rebalancing for downtime at STA 1 on day 3 with 2 hours downtime
rebalanced_station_efficiency = rebalance_for_downtime('STA 1', 3, 2, station_efficiency, employee_count)
rebalanced_station_efficiency_df = pd.DataFrame(rebalanced_station_efficiency).T
print(rebalanced_station_efficiency_df)

# Function to plot the number of operations completed over time
def plot_operations_over_time(operation_df):
    fig = px.line(operation_df, x='End Time', y=operation_df.index, title='Number of Operations Completed Over Time', labels={'index': 'Operations Completed', 'End Time': 'Time'})
    fig.show()

# Function to plot the number of vehicles at each station over time
def plot_vehicles_per_station(line_moves_df):
    station_counts = line_moves_df.groupby(['Time', 'To Station']).size().reset_index(name='Count')
    fig = px.scatter(station_counts, x='Time', y='To Station', size='Count', title='Vehicles at Each Station Over Time', labels={'Count': 'Number of Vehicles'})
    fig.show()

# Function to plot HPU per station
def plot_hpu_per_station(station_efficiency_df):
    fig = px.bar(station_efficiency_df, x=station_efficiency_df.index, y='HPU', title='HPU per Station', labels={'index': 'Station', 'HPU': 'Hours per Unit'})
    fig.show()

# Function to plot operator assignments
def plot_operator_assignments(assignments_df):
    fig = px.bar(assignments_df, x='Day', y='Assigned Operators', color='Station', title='Operator Assignments per Day', labels={'Assigned Operators': 'Number of Operators'})
    fig.show()

# Generate plots
plot_operations_over_time(operation_df)
plot_vehicles_per_station(line_moves_df)
plot_hpu_per_station(station_efficiency_df)
plot_operator_assignments(assignments_df)

# Calculate downtime impact
def calculate_downtime_impact(line_moves_df, downtime, run_time, shift_duration):
    total_simulation_time = run_time * shift_duration
    downtime_impact = []
    
    for station, (start_time, duration) in downtime.items():
        downtime_percentage = (duration / total_simulation_time) * 100
        downtime_impact.append({
            'Station': station,
            'Downtime Hours': duration,
            'Downtime Percentage': downtime_percentage
        })
    
    downtime_impact_df = pd.DataFrame(downtime_impact)
    return downtime_impact_df

# Calculate employee utilization
def calculate_employee_utilization(daily_operator_requirements_df, employee_count, shift_duration):
    total_simulation_hours = len(daily_operator_requirements_df) * shift_duration * employee_count
    active_hours = daily_operator_requirements_df['Available Employees'].sum() * shift_duration
    utilization_percentage = (active_hours / total_simulation_hours) * 100
    
    return {
        'Total Simulation Hours': total_simulation_hours,
        'Active Hours': active_hours,
        'Utilization Percentage': utilization_percentage
    }

# Generate downtime impact analysis
downtime_impact_df = calculate_downtime_impact(line_moves_df, downtime, run_time, shift_duration)
print(downtime_impact_df)

# Generate employee utilization analysis
employee_utilization = calculate_employee_utilization(daily_operator_requirements_df, employee_count, shift_duration)
print(employee_utilization)

# Function to plot downtime impact
def plot_downtime_impact(downtime_impact_df):
    fig = px.bar(downtime_impact_df, x='Station', y='Downtime Hours', title='Downtime Impact per Station', labels={'Downtime Hours': 'Downtime (Hours)'})
    fig.show()

# Function to plot employee utilization
def plot_employee_utilization(employee_utilization):
    labels = ['Active Hours', 'Idle Hours']
    values = [employee_utilization['Active Hours'], employee_utilization['Total Simulation Hours'] - employee_utilization['Active Hours']]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Employee Utilization')
    fig.show()

# Generate plots
plot_downtime_impact(downtime_impact_df)
plot_employee_utilization(employee_utilization)
