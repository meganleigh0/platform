def save_station_requirements_to_csv(schedule, filename='station_requirements.csv'):
    data = []

    for program_key, program_obj in schedule.programs.items():
        program_name = program_obj.name
        for month in schedule.months:
            quantity = program_obj.get_quantity_for_month(month)
            if quantity > 0:
                for station_name, station_hours in program_obj.product_station_req.items():
                    data.append({
                        'Program': program_name,
                        'Month': month,
                        'Station Name': station_name,
                        'Station Hours': station_hours * quantity
                    })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def save_department_requirements_to_csv(schedule, filename='department_requirements.csv'):
    data = []

    for program_key, program_obj in schedule.programs.items():
        program_name = program_obj.name
        for month in schedule.months:
            quantity = program_obj.get_quantity_for_month(month)
            if quantity > 0:
                for dept_id, dept_hours in program_obj.product_department_req.items():
                    data.append({
                        'Program': program_name,
                        'Month': month,
                        'Department ID': dept_id,
                        'Department Hours': dept_hours * quantity
                    })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Example usage
# save_department_requirements_to_csv(schedule)
