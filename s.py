class Scheduler:
    def __init__(self, env, schedule, plant_simulation):
        self.env = env
        self.schedule = schedule
        self.plant_simulation = plant_simulation

    def run_day(self, production_months):
        for month in production_months:
            for (program, mbom), program_instance in self.schedule.programs.items():
                qty = program_instance.get_quantity_for_month(month)
                for _ in range(qty):
                    structure = self.plant_simulation.induce_structure()
                    product = load_product(self.env, mbom)
                    self.env.process(self.plant_simulation.process(structure, product))
        self.env.run(8)
