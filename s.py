import simpy
import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar

class Operator:
    def __init__(self, operator_id):
        self.operator_id = operator_id
        self.available = True

class Hull:
    def __init__(self, hull_id):
        self.hull_id = hull_id
        self.current_station = "STA 0"
        self.operations_completed = {}

class Line:
    def __init__(self, env, stations, operators, hulls, operations, start_date, production_rate):
        self.env = env
        self.stations = stations
        self.operators = operators
        self.hulls = hulls
        self.operations = operations
        self.start_date = pd.Timestamp(start_date)
        self.production_rate = production_rate
        self.operation_log = []
        self.floor_status = {}
        self.floor_df = pd.DataFrame()

    def run_line(self):
        while True:
            for hull in list(self.hulls):
                for operation in self.operations:
                    if hull.current_station == operation['station'] and not hull.operations_completed.get(operation['name'], False):
                        if self.stations[operation['station']].count < 3:
                            with self.stations[operation['station']].request() as req:
                                yield req
                                start_time = self.env.now
                                yield self.env.timeout(operation['hours'])
                                hull.operations_completed[operation['name']] = True
                                available_operators = [op for op in self.operators if op.available]
                                if available_operators:
                                    operator = np.random.choice(available_operators)
                                    operator.available = False
                                else:
                                    operator = None
                                self.operation_log.append({
                                    'hull_id': hull.hull_id,
                                    'operation': operation['name'],
                                    'start_time': start_time,
                                    'end_time': self.env.now,
                                    'station': operation['station'],
                                    'operator_id': operator.operator_id if operator else None,
                                    'day': (self.start_date + pd.Timedelta(hours=self.env.now)).strftime('%Y-%m-%d')
                                })
                                if all(hull.operations_completed.get(op['name'], False) for op in self.operations if op['station'] == hull.current_station):
                                    current_index = int(hull.current_station.split()[1])
                                    next_station = f"STA {current_index + 1}" if current_index < 17 else None
                                    if next_station:
                                        hull.current_station = next_station
                                        hull.operations_completed = {}
            yield self.env.timeout(8 / self.production_rate)

    def assign_operators(self):
        while True:
            self.floor_status = {station: None for station in self.stations}
            for hull in self.hulls:
                self.floor_status[hull.current_station] = hull.hull_id
            self.floor_df = pd.concat([self.floor_df, pd.DataFrame([self.floor_status])], ignore_index=True)
            day_of_week = (self.start_date + pd.Timedelta(hours=self.env.now)).dayofweek
            attrition_factor = attrition_rates.get(day_of_week, 0.05)
            for operator in self.operators:
                if operator.available and np.random.rand() < attrition_factor:
                    operator.available = False
            yield self.env.timeout(8)  # Recalculate at the end of each shift

env = simpy.Environment()
stations = {f"STA {i}": simpy.Resource(env, capacity=1) for i in range(18)}
operators = [Operator(i) for i in range(10)]
hulls = [Hull(i) for i in range(10)]
operations = [
    {"name": "Operation 1", "station": "STA 0", "hours": 3},
    {"name": "Operation 2", "station": "STA 1", "hours": 2},
    {"name": "Operation 3", "station": "STA 0", "hours": 1},
    {"name": "Operation 4", "station": "STA 2", "hours": 4}
]
attrition_rates = {0: 0.05, 1: 0.2, 2: 0.05, 3: 0.05, 4: 0.1, 5: 0.2, 6: 0.1}  # Monday and Friday higher attrition

production_line = Line(env, stations, operators, hulls, operations, start_date='2023-01-01', production_rate=1.0)
env.process(production_line.run_line())
env.process(production_line.assign_operators())
env.run(until=24 * 365)  # Run the simulation for one year

# Output operation log
for log in production_line.operation_log:
    print(log)
# Output floor status DataFrame for review
print(production_line.floor_df)
