class Scheduler:
    def __init__(self, schedule, day_rate):
        self.schedule = schedule
        self.day_rate = day_rate
        self.current_day = 1
        self.current_month = 0
        self.monthly_production_complete = False

    def run_for_a_day(self, env, plant_simulation):
        if not self.monthly_production_complete:
            for _ in range(self.day_rate):
                program, mbom = self.get_next_program()
                if program:
                    structure = plant_simulation.induce_structure()
                    product = load_product(env, mbom)
                    env.process(plant_simulation.process(structure, product))
            self.current_day += 1
            self.check_month_completion()
        else:
            print("Monthly production already complete.")

    def run_for_a_month(self, env, plant_simulation):
        while not self.monthly_production_complete:
            self.run_for_a_day(env, plant_simulation)

    def check_month_completion(self):
        if self.current_day > len(production_months[self.current_month]):
            self.monthly_production_complete = True
            self.current_day = 1
            self.current_month += 1
            if self.current_month >= len(production_months):
                print("Production for all months complete.")
            else:
                self.monthly_production_complete = False

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

scheduler = Scheduler(schedule, day_rate=1)

# Example of running day by day
for day in range(30):  # Assuming a 30-day month
    scheduler.run_for_a_day(env, plant_simulation)

# Example of running for the entire month
scheduler.run_for_a_month(env, plant_simulation)

env.run(160)
