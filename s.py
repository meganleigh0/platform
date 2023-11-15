class Scheduler:
    SHIFT_DURATION = 8  # 8 hours shift

    def __init__(self, env, schedule, day_rate, plant_simulation):
        self.env = env
        self.schedule = schedule
        self.day_rate = day_rate
        self.plant_simulation = plant_simulation
        self.current_month = 0

    def run_for_a_day(self):
        start_time = self.env.now
        shift_end = start_time + self.SHIFT_DURATION

        while self.env.now < shift_end:
            for _ in range(self.day_rate):
                if not self.has_pending_processes():
                    return  # No more processes to start for the day

                program, mbom = self.get_next_program()
                if program:
                    structure = self.plant_simulation.induce_structure()
                    product = load_product(self.env, mbom)
                    self.env.process(self.plant_simulation.process(structure, product))

            yield self.env.timeout(1)  # Wait for an hour before checking again

    def has_pending_processes(self):
        for (program, mbom), program_obj in self.schedule.programs.items():
            month = production_months[self.current_month]
            if program_obj.get_quantity_for_month(month) > 0:
                return True
        return False

    def get_next_program(self):
        for (program, mbom), program_obj in this.schedule.programs.items():
            month = production_months[this.current_month]
            qty = program_obj.get_quantity_for_month(month)
            if qty > 0:
                program_obj.production_plan[month] -= 1
                return program, mbom
        return None, None

    def run_for_a_month(self):
        for day in range(30):  # Assuming a 30-day month
            self.env.process(self.run_for_a_day())
            self.env.run(until=self.env.now + self.SHIFT_DURATION)
            self.current_month += 1 / 30  # Increment the month fractionally