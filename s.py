   # Step 1: Ensure every station with a Hull has at least one operator
        for station_name, station in self.stations.items():
            if isinstance(station.stand, Hull) and len(station.operators) == 0 and self.operators:
                operator = self.operators.pop(0)
                station.operators.append(operator)
                print(f"Assigned operator {operator} to station {station_name}")

        # Step 2: Distribute remaining operators up to the capacity of each station
        for station_name, station in self.stations.items():
            while len(station.operators) < station.operator_capacity.capacity and self.operators:
                operator = self.operators.pop(0)
                station.operators.append(operator)
                print(f"Assigned operator {operator} to station {station_name}")
