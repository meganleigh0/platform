import pandas as pd

# Initialize DataFrame and dictionary to store completed counts
df = pd.DataFrame(assembly_logger.log)
completed_count = {f'{month}': {} for month in range(20)}

# Constants for easier configuration
TIME_PERIOD = 160
PROGRAMS = ['Taiwan', 'Australia', 'Sep 90a', 'Sep 90b', 'Poland']
ASSEMBLY_STEPS = ['prep and ship', 'prep ship']

# Processing the data
for month in range(20):
    # Filter DataFrame for the current time period
    month_filter = (df['Timestamp'] < (month + 1) * TIME_PERIOD) & (df['Timestamp'] >= month * TIME_PERIOD)
    month_df = df[month_filter]

    # Further filtering for relevant assembly steps and interaction
    relevant_df = month_df[(month_df['Assembly'].isin(ASSEMBLY_STEPS)) & (month_df['Interaction'] == 'end')]

    # Count occurrences
    for _, row in relevant_df.iterrows():
        vehicle_type = row['Vehicle'].split(':')[0]
        completed_count[f'{month}'].setdefault(vehicle_type, 0)
        completed_count[f'{month}'][vehicle_type] += 1

    # Ensure all programs are represented in the dictionary, even if count is zero
    for program in PROGRAMS:
        completed_count[f'{month}'].setdefault(program, 0)

    # Cumulate counts from previous months
    if month != 0:
        for program in completed_count[f'{month}']:
            completed_count[f'{month}'][program] += completed_count[f'{month - 1}'].get(program, 0)

    # Add the vehicles completed prior to May 2024 for each program
    additions = {'Taiwan': 23, 'Sep 90a': 42, 'Australia': 21}
    for program, additional_units in additions.items():
        if program in completed_count[f'{month}']:
            completed_count[f'{month}'][program] += additional_units

# Convert to DataFrame and set columns
complete = pd.DataFrame(completed_count).T
production_months = [f'{m} 2024' for m in ["May", "June", "July", "August", "September", "October"]]
complete.columns = production_months[:len(complete.columns)]

# Formatting options
pd.options.display.float_format = '{:,.0f}'.format
pd.set_option('display.max_columns', None)

# Display the DataFrame
complete.fillna(0)