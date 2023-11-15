import simpy

class Scheduler:
    SHIFT_DURATION = 8  # 8 hours

    def __init__(self, env, schedule, day_rate):
        self.env = env
        self.schedule = schedule
        self.day_rate = day_rate
        self.current_day = 1
        self.current_month = 0

    def start(self):
        self.env.process(self.run_schedule())

    def run_schedule(self):
        while self.current_month < len(production_months):
            yield self.env.process(self.run_for_a_month())
            self.current_month += 1
            self.current_day = 1

    def run_for_a_month(self):
        while self.current_day <= len(production_months[self.current_month]):
            yield self.env.process(self.run_for_a_day())
            self.current_day += 1

    def run_for_a_day(self):
        start_time = self.env.now
        for shift in range(24 // self.SHIFT_DURATION):  # Number of shifts in a day
            for _ in range(self.day_rate):
                program, mbom = self.get_next_program()
                if program:
                    structure = plant_simulation.induce_structure()
                    product = load_product(self.env, mbom)
                    self.env.process(plant_simulation.process(structure, product))
            # Wait for the next shift
            yield self.env.timeout(start_time + self.SHIFT_DURATION * (shift + 1) - self.env.now)

    def get_next_program(self):
        for (program, mbom), program_obj in self.schedule.programs.items():
            month = production_months[self.current_month]
            qty = program_obj.get_quantity_for_month(month)
            if qty > 0:
                program_obj.production_plan[month] -= 1
                return program, mbom
        return None, None

# Usage in your simulation
env = simpy.Environment()
schedule = Schedule()
schedule = schedule.load_schedule()
plant_simulation = Plant(env)

scheduler = Scheduler(env, schedule, day_rate=2)  #⬤