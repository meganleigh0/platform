import pandas as pd

# Assuming you have the following DataFrames and dictionary as described:
# programs, dep, and mom_dep_regs

# Aggregate vehicle quantities by month, family, and mbom
monthly_mbom_quantities = programs.groupby(['Month', 'Family', 'mbom']).agg({'Vehicles': 'sum'}).reset_index()

# Initialize an empty DataFrame to hold the computed department hours for each month
dept_monthly_hours = pd.DataFrame()

# Iterate over each month to calculate required department hours based on vehicle production
for month in months:
    this_month_req = monthly_mbom_quantities[monthly_mbom_quantities["Month"] == month]
    
    # Initialize an empty DataFrame to collect this month's departmental hours requirements
    this_month_labor = pd.DataFrame()

    # Iterate over each row in the monthly requirements DataFrame
    for index, row in this_month_req.iterrows():
        mbom = row['mbom']
        vehicles = row['Vehicles']
        
        # Retrieve the department hour requirements for this mbom from the dictionary
        if mbom in mom_dep_regs:
            mbom_dep_reqs = mom_dep_regs[mbom]
            
            # Calculate the total hours for each department based on the number of vehicles
            vehicles_mbom_dep_reqs = mbom_dep_reqs * vehicles
            vehicles_mbom_dep_reqs = vehicles_mbom_dep_reqs.reset_index()
            vehicles_mbom_dep_reqs.rename(columns={mbom_dep_reqs.name: 'RequiredHours'}, inplace=True)
            vehicles_mbom_dep_reqs['Month'] = month
            
            # Append the results to the month's DataFrame
            this_month_labor = pd.concat([this_month_labor, vehicles_mbom_dep_reqs], ignore_index=True)

    # Aggregate hours by DEPT and Month if there is any data
    if not this_month_labor.empty:
        this_month_labor = this_month_labor.groupby(['DEPT', 'Month']).agg({'RequiredHours': 'sum'}).reset_index()
        dept_monthly_hours = pd.concat([dept_monthly_hours, this_month_labor], ignore_index=True)

# Now dept_monthly_hours contains the aggregated required hours by department and month
# Compare it with actual department hours from 'dep' DataFrame
comparison = dept_monthly_hours.merge(dep, on=['DEPT', 'Month'], how='left')
comparison['HoursVariance'] = comparison['RequiredHours'] - comparison['EstimatedHours']

print(comparison)