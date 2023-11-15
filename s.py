class Scheduler:
    SHIFT_DURATION = 8  # 8 hours shift

    def __init__(self, env, schedule, day_rate):
        # ... [other attributes]
        self.shift_end = 0

    def run_for_a_day(self):
        self.shift_end = self.env.now + self.SHIFT_DURATION
        while self.env.now < self.shift_end:
            if not self.has_pending_processes():
                break

            program, mbom = self.get_next_program()
            if program:
                structure = plant_simulation.induce_structure()
                product = load_product(self.env, mbom)
                process_duration = self.get_process_duration(program)  # Define this method based on your logic
                yield self.env.process(plant_simulation.process(structure, product, process_duration))
            else:
                yield self.env.timeout(1)  # Wait for an hour before checking again

    def has_pending_processes(self):
        # Check if there are any pending processes that need to be started in the current shift
        for (program, mbom), program_obj in self.schedule.programs.items():
            month = production_months[self.current_month]
            if program_obj.get_quantity_for_month(month) > 0:
                return True
        return False

    # ... [rest of the class]

# Usage in your simulation
env = simpy.Environment()
# ... [setup your schedule and plant_simulation]
scheduler = Scheduler(env, schedule, day_rate=1)
scheduler.run_for_a_day()
env.run()