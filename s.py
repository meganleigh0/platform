import datetime

class Scheduler:
    def __init__(self, schedule, env, start_date=datetime.date(2025, 1, 1)):
        self.schedule = schedule
        self.env = env
        self.current_date = start_date

    def is_weekend(self, date):
        return date.weekday() > 4  # 5 and 6 correspond to Saturday and Sunday

    def process_product(self, program_obj):
        product = load_product(self.env, program_obj.mbom)
        self.env.process(product.process())  # Start the product process

    def run_for_a_day(self, day_rate):
        for month in self.schedule.months:
            for program, program_obj in self.schedule.programs.items():
                quantity_needed = program_obj.get_quantity_for_month(month)
                if quantity_needed > 0:
                    for _ in range(min(day_rate, quantity_needed)):
                        self.process_product(program_obj)
                        program_obj.update_production_plan(month, quantity_needed - 1)
                    break  # Move to next day after processing up to day_rate products

    def run(self, day_rate, days_to_run):
        for _ in range(days_to_run):
            if not self.is_weekend(self.current_date):
                self.run_for_a_day(day_rate)
                self.env.run(until=self.env.now + 8)  # Simulate 8 hours of work
            self.current_date += datetime.timedelta(days=1)

# Usage remains the same
