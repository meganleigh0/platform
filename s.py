def calculate_total_hours(operations_list):
    # Initialize a dictionary to store total hours per department
    department_hours = {}

    # Process each assembly
    for assembly in operations_list:
        # Flatten the assembly's operations
        flattened_operations = [op for op in assembly]

        # Process each operation in the assembly
        for operation in flattened_operations:
            hours, name, department = operation
            hours = float(hours)  # Convert hours to a float

            # Add hours to the respective department
            if department in department_hours:
                department_hours[department] += hours
            else:
                department_hours[department] = hours

    return department_hours
