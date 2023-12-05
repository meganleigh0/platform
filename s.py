import datetime

class Scheduler:
    def __init__(self, schedule, env, start_date=datetime.date(2025, 1, 1)):
        self.schedule = schedule
        self.env = env
        self.current_date = start_date

    def is_weekend(self, date):
        return date.weekday() > 4  # 5 and 6 correspond to Saturday and Sunday

    def run_for_a_day(self, day_rate):
        for month in self.schedule.months:
            for program, program_obj in self.schedule.programs.items():
                quantity_needed = program_obj.get_quantity_for_month(month)
                if quantity_needed > 0:
                    product = load_product(self.env, program_obj.mbom)
                    self.env.process(product.process())
                    program_obj.update_production_plan(month, quantity_needed - 1)
                    if day_rate == 2 and quantity_needed > 1:
                        product = load_product(self.env, program_obj.mbom)
                        self.env.process(product.process())
                        program_obj.update_production_plan(month, quantity_needed - 2)
                    break  # Move to next day after processing day_rate products

    def run(self, day_rate, days_to_run):
        for _ in range(days_to_run):
            if not self.is_weekend(self.current_date):
                self.run_for_a_day(day_rate)
            self.current_date += datetime.timedelta(days=1)
            self.env.run()  # Run the simulation for the current day
