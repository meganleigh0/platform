# Sort stations by the size of the operation queue and total processing time in descending order
        sorted_stations = sorted(
            self.stations.values(), 
            key=lambda s: (len(s.operation_queue.items), sum(op.time for op in s.operation_queue.items)), 
            reverse=True
        )
