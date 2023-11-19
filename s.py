class Scheduler:
    def __init__(self, env, schedule, plant_simulation, day_rate):
        self.env = env
        self.schedule = schedule
        self.plant_simulation = plant_simulation
        self.day_rate = day_rate

    def run_program(self, program_instance, mbom, month):
        total_qty = program_instance.get_quantity_for_month(month)
        program_start_time = self.env.now
        while total_qty > 0:
            daily_qty = min(self.day_rate, total_qty)
            for _ in range(daily_qty):
                structure = self.plant_simulation.induce_structure()
                product = load_product(self.env, mbom)
                self.env.process(self.plant_simulation.process(structure, product))
            total_qty -= daily_qty
            self.env.run(8)
        program_duration = self.env.now - program_start_time
        print(f"Program {program_instance.name} completed in {program_duration} hours.")

    def run_day(self, production_months):
        for month in production_months:
            for (program, mbom), program_instance in self.schedule.programs.items():
                self.run_program(program_instance, mbom, month)

    def run_month(self, production_months):
        for _ in range(20):  # Assuming 20 working days in a month
            self.run_day(production_months)
