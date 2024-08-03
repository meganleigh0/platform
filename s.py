import simpy
import numpy as np
import pandas as pd

class Operator:
    def __init__(self, env, operator_id):
        self.env = env
        self.operator_id = operator_id
        self.current_assignment = None

    def perform_operation(self, station):
        while True:
            if len(station.operation_queue.items) == 0:
                print(f"{self.operator_id} has no more operations to perform at {station.station_id}")
                break

            current_time = self.env.now
            operation = yield station.operation_queue.get()
            remaining_shift_time = 8 - (current_time % 8)

            if operation.hours <= remaining_shift_time:
                print(f"{self.operator_id} at {station.station_id} is performing operation taking {operation.hours} time units.")
                yield self.env.timeout(operation.hours)
            else:
                # If not enough time in the shift, put the operation back and break to end the current shift
                print(f"{self.operator_id} at {station.station_id} cannot start operation taking {operation.hours} time units due to insufficient time in the shift.")
                yield station.operation_queue.put(operation)
                break

            print(f"{self.operator_id} completed operation at {station.station_id}")

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
        self.rate = 1.25
        self.shift_duration = 8
        self.operators = [Operator(env, f"Operator_{i}") for i in range(self.head_count)]
        self.log = []
        self.assigned_operators = []

        # Initialization
        self.initialize_hulls()
        for station, (start_time, duration) in downtime.items():
            self.stations[station].add_downtime(start_time, duration)

    def initialize_hulls(self):
        for _, row in self.floor_status.iterrows():
            station = self.stations[row['Station']]
            hull = Hull(self.env, row['Vin'], row['Program'], self.operation_data)
            hull.current_state = row['Station']
            station.accept_hull(hull)

    def run_line(self):
        while True:
            # Start of shift
            self.resample_headcount()
            self.assign_shift_operators()
            self.work_operators()
            yield self.env.timeout(self.shift_duration)
            # End of shift
            self.log_floor_status()
            self.release_operators()

    def work_operators(self):
        for operator, station in self.assigned_operators:
            self.env.process(operator.perform_operation(station))

    def resample_headcount(self):
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][int(self.env.now // self.shift_duration) % 5]
        min_attrition, max_attrition = self.attrition_rates[day_of_week]
        attrition_rate = np.random.uniform(min_attrition, max_attrition)
        available_headcount = int(self.head_count * (1 - attrition_rate))
        self.operators = [Operator(self.env, f"Operator_{i}") for i in range(available_headcount)]
        print(f"Resampled headcount: {available_headcount} operators available on {day_of_week}")

    def assign_shift_operators(self):
        # Filter out stations without a Hull in the stand or with no operations
        eligible_stations = [s for s in self.stations.values() if isinstance(s.stand, Hull) and len(s.operation_queue.items) > 0]

        # Sort stations by the size of the operation queue and total processing time in descending order
        sorted_stations = sorted(
            eligible_stations,
            key=lambda s: (len(s.operation_queue.items), sum(op.hours for op in s.operation_queue.items)),
            reverse=True
        )

        # Ensure every station with a Hull has at least one operator
        for station in sorted_stations:
            if len(station.operators) == 0 and self.operators:
                operator = self.operators.pop(0)
                station.operators.append(operator)
                self.assigned_operators.append((operator, station))
                print(f"Assigned operator {operator} to station {station.station_id}")

        # Distribute remaining operators up to the capacity of each station based on priority
        while self.operators:
            for station in sorted_stations:
                if self.operators and len(station.operators) < station.operator_capacity.capacity:
                    operator = self.operators.pop(0)
                    station.operators.append(operator)
                    self.assigned_operators.append((operator, station))
                    print(f"Assigned operator {operator} to station {station.station_id}")

    def release_operators(self):
        for operator, station in self.assigned_operators:
            station.operators.remove(operator)
            self.operators.append(operator)
            print(f"Released operator {operator} from station {station.station_id}")
        self.assigned_operators.clear()

    def log_floor_status(self):
        status = {station: (self.stations[station].stand.hull_id if self.stations[station].stand else None) for station in self.stations}
        self.log.append((self.env.now, status))
        print(f"Floor status at time {self.env.now}: {status}")

class Station:
    def __init__(self, env, station_id):
        self.env = env
        self.station_id = station_id
        self.operation_queue = simpy.Store(env)
        self.operator_capacity = simpy.Resource(env, capacity=3)
        self.stand = None
        self.operators = []
        self.current_operations = []

    def accept_hull(self, hull):
        self.stand = hull
        operations = hull.get_station_operations()
        for _, row in operations.iterrows():
            operation = Operation(self.env, row['Operation Title'], row['Hours'])
            self.operation_queue.put(operation)

    def add_downtime(self, start_time, duration):
        self.downtime.append((start_time, duration))

class Hull:
    def __init__(self, env, hull_id, program, operation_data):
        self.env = env
        self.hull_id = hull_id
        self.program = program
        self.operation_data = operation_data
        self.current_state = None

    def get_station_operations(self):
        if self.operation_data is not None:
            program_data = self.operation_data[self.operation_data['Program'] == self.program].copy()
            return program_data[program_data['Station'] == self.current_state]

class Operation:
    def __init__(self, env, title, hours):
        self.env = env
        self.title = title
        self.hours = hours

# Simulation Parameters
available_hulls = [
    {'HullID': 'Hull1A', 'Program': 'SEPVP3'},
    {'HullID': 'Hull2A', '​⬤