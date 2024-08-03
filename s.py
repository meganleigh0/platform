    def assign_shift_operators(self):
        # Sort stations by the size of the operation queue and processing time in descending order
        sorted_stations = sorted(self.stations.values(), key=lambda s: (len(s.operation_queue), s.processing_time), reverse=True)
        
        # Step 1: Ensure every station with a Hull has at least one operator
        for station in sorted_stations:
            if isinstance(station.stand, Hull) and len(station.operators) == 0 and self.operators:
                operator = self.operators.pop(0)
                station.operators.append(operator)
                self.assigned_operators.append((operator, station))
                print(f"Assigned operator {operator} to station {station.name}")

        # Step 2: Distribute remaining operators up to the capacity of each station based on priority
        while self.operators:
            for station in sorted_stations:
                if self.operators and len(station.operators) < station.operator_capacity.capacity:
                    operator = self.operators.pop(0)
                    station.operators.append(operator)
                    self.assigned_operators.append((operator, station))
                    print(f"Assigned operator {operator} to station {station.name}")
