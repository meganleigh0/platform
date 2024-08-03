   def start_operators(self):
        # Start the operators' tasks in parallel
        for operator, station in self.assigned_operators:
            self.env.process(self.perform_operation(operator, station))

    def perform_operation(self, operator, station):
        # Operator performs operations from the station's queue
        while True:
            if len(station.operation_queue.items) == 0:
                break
            operation = yield station.operation_queue.get()
            print(f"{operator} at {station.name} is performing operation taking {operation.time} time units at time {self.env.now}.")
            yield self.env.timeout(operation.time)
