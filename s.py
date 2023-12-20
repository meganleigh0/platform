import pandas as pd

def save_schedule_requirements_to_csv(schedule, filename='schedule_requirements.csv'):
    data = []

    for program_key, program_obj in schedule.programs.items():
        program_name = program_obj.name
        for month in schedule.months:
            quantity = program_obj.get_quantity_for_month(month)
            if quantity > 0:
                for dept_id, dept_hours in program_obj.product_department_req.items():
                    for station_name, station_hours in program_obj.product_station_req.items():
                        data.append({
                            'Program': program_name,
                            'Month': month,
                            'Department ID': dept_id,
                            'Station Name': station_name,
                            'Department Hours': dept_hours * quantity,
                            'Station Hours': station_hours * quantity
                        })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Example usage
# Assuming you have a 'schedule' object from your Schedule class
save_schedule_requirements_to_csv(schedule)
