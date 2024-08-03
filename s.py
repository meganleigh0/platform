def attempt_transition(self):
    while True:
        for station_name in sorted(self.stations.keys(), reverse=True):
            station = self.stations[station_name]
            # Allow transition only if next station is empty and running and current station has no operations left
            if station.stand and isinstance(station.stand, Hull) and not station.is_down() and not station.operation_queue.items:
                next_station_name = self.get_next_station(station_name)
                if next_station_name:
                    next_station = self.stations[next_station_name]
                    if not next_station.stand and not next_station.is_down():
                        hull = station.stand
                        # Check if all operations in the current station are completed
                        if hull.get_station_operations() == []:
                            station.stand = None
                            hull.move_to_next_state(next_station_name)
                            next_station.stand = hull
                            next_station.accept_hull(hull)
                            self.completion_queue.append(completed_hull)
                            if completed_hull.program not in self.completed_hulls:
                                self.completed_hulls[completed_hull.program] = 0
                            self.completed_hulls[completed_hull.program] += 1
                            print(f"Hull {completed_hull.hull_id} completed at {station_name} at time {self.env.now()}")
        yield self.env.timeout(self.shift_duration / self.rate)