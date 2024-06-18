import pandas as pd

# Assume the DataFrames 'programs' and dictionary 'mom_dep_regs' are correctly defined.

# Aggregate vehicle quantities by month, family, and mbom
monthly_mbom_quantities = programs.groupby(['Month', 'Family', 'mbom']).agg({'Vehicles': 'sum'}).reset_index()

# Initialize an empty DataFrame to hold the total required hours for each department by month
total_required_hours = pd.DataFrame()

# Loop through each month to calculate the required department hours
for month in months:
    # Filter records for this specific month
    this_month_req = monthly_mbom_quantities[monthly_mbom_quantities['Month'] == month]
    
    # Initialize a list to store DataFrame for each mbom's required hours this month
    dept_hours_list = []

    for _, row in this_month_req.iterrows():
        mbom = row['mbom']
        vehicles = row['Vehicles']

        # Get the department hour requirements for this mbom if it exists in the dictionary
        if mbom in mom_dep_regs:
            # Retrieve the DataFrame for this mbom from the dictionary and calculate required hours
            mbom_hours = mom_dep_regs[mbom].copy()
            mbom_hours['RequiredHours'] = mbom_hours * vehicles  # Multiply hours needed by number of vehicles

            # Add the month column to mbom_hours DataFrame
            mbom_hours['Month'] = month
            dept_hours_list.append(mbom_hours)

    # Concatenate all mbom hours data for this month and sum hours for the same department
    if dept_hours_list:
        month_hours_df = pd.concat(dept_hours_list)
        month_hours_df = month_hours_df.groupby(['DEPT', 'Month']).agg({'RequiredHours': 'sum'}).reset_index()
        total_required_hours = pd.concat([total_required_hours, month_hours_df], ignore_index=True)

# Check if the DataFrame 'total_required_hours' is empty and print the results
if not total_required_hours.empty:
    print(total_required_hours)
else:
    print("No data available for the specified months or mbom configurations.")