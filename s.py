Class Definitions
Hull Class
python
Copy code
import simpy

class Hull:
    def __init__(self, env, hull_id, program):
        self.env = env
        self.hull_id = hull_id
        self.program = program
        self.current_station = None

    def move_to_next_station(self, next_station):
        self.current_station = next_station
        print(f'Time {self.env.now}: Hull {self.hull_id} moved to {self.current_station}')

    def log_movement(self, from_station, to_station):
        print(f'Time {self.env.now}: Hull {self.hull_id} moved from {from_station} to {to_station}')
Station Class
python
Copy code
class Station:
    def __init__(self, env, station_id):
        self.env = env
        self.station_id = station_id
        self.current_hull = None
        self.operators = []

    def assign_operator(self, operator):
        if len(self.operators) < 3:
            self.operators.append(operator)
            print(f'Time {self.env.now}: Operator {operator.operator_id} assigned to {self.station_id}')
        else:
            print(f'Time {self.env.now}: Station {self.station_id} is full')

    def start_operation(self, operation, hours, operator):
        yield self.env.timeout(hours)
        self.complete_operation(operation, operator)

    def complete_operation(self, operation, operator):
        print(f'Time {self.env.now}: Operation {operation} completed by Operator {operator.operator_id} at {self.station_id}')

    def handle_downtime(self, duration):
        yield self.env.timeout(duration)
        print(f'Time {self.env.now}: Station {self.station_id} downtime ended')
AssemblyLine Class
python
Copy code
class AssemblyLine:
    def __init__(self, env, stations, hulls, employees, shift_schedule, downtimes):
        self.env = env
        self.stations = stations
        self.hulls = hulls
        self.employees = employees
        self.shift_schedule = shift_schedule
        self.downtimes = downtimes
        self.logs = {
            'operation_table': [],
            'floor_status': [],
            'line_movement': [],
            'operator_assignment': []
        }

    def initialize_line(self):
        for station in self.stations:
            station.current_hull = None

    def assign_shifts(self):
        # Assign operators to shifts dynamically
        pass

    def process_day(self):
        # Process each day, including attrition, shifts, and operations
        pass

    def apply_attrition(self, day):
        attrition_rate = self.shift_schedule['attrition'][day]
        self.employees = int(self.employees * (1 - attrition_rate))
        print(f'Time {self.env.now}: Applied attrition, employees remaining: {self.employees}')

    def log_results(self):
        # Log the results for each operation, floor status, line movement, and operator assignment
        pass

    def run_simulation(self, days):
        for day in range(days):
            self.apply_attrition(day)
            self.process_day()
            self.log_results()
Simulation Logic
Initialize Parameters
python
Copy code
import pandas as pd

# Example DataFrames for operations, hulls, and employees
operation_data = pd.DataFrame({
    'Station': ['STA 0', 'STA 0', 'STA 0', 'STA 1', 'STA 1', 'STA 2'],
    'Operation': ['Build', 'Assemble', 'Assemble', 'Tear', 'Dry', 'Paint'],
    'Hours': [0.23, 1.3, 0.3, 0.5, 1.0, 3.0],
    'Program': ['A', 'B', 'B', 'A', 'A', 'A']
})

available_hulls = pd.DataFrame({
    'HullID': ['Hull1', 'Hull2', 'Hull3'],
    'Program': ['A', 'B', 'C']
})

shift_schedule = {
    'standard_shift': 8,
    'standard_week': 40,
    'monthly': 160,
    'attrition': {'Monday': 0.1, 'Tuesday': 0.1, 'Wednesday': 0.1, 'Thursday': 0.1, 'Friday': 0.3, 'Saturday': 0.1, 'Sunday': 0.1}
}

downtimes = {'STA 0': (5, 2)}  # Example: Downtime starts at hour 5 and lasts for 2 hours
Running the Simulation
python
Copy code
# Initialize environment and components
env = simpy.Environment()
stations = [Station(env, f'STA {i}') for i in range(18)]
hulls = [Hull(env, row['HullID'], row['Program']) for index, row in available_hulls.iterrows()]
employees = 10  # Example headcount

assembly_line = AssemblyLine(env, stations, hulls, employees, shift_schedule, downtimes)

# Run the simulation for a given number of days
env.process(assembly_line.run_simulation(5))  # Run for 5 days as an example
env.run()
Notes:
The assign_shifts, process_day, and log_results methods need detailed implementations to match your specific logic for handling shifts, operations, and logging.
The handle_downtime method in the Station class should be linked to actual downtime events affecting the station.
The apply_attrition method adjusts the employee count dynamically based on attrition rates.
The run_simulation method orchestrates the overall simulation process, handling day-by-day operations.
