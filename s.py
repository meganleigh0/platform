import pandas as pd

# Initialize DataFrame from log
main_df = pd.DataFrame(dept_logger.log)
main_df = main_df.sort_values(['Operation ID', 'Timestamp'])

# Constants
TIME_SLOT = 8  # Each time slot duration
total_periods = int(end // TIME_SLOT) + 1  # Total number of time periods

# Initialize list to store total man-hours for each period
daily_hours = []

# Loop through each period
for k in range(total_periods):
    # Filter DataFrame for current time slot
    time_filter = (main_df['Timestamp'] >= k * TIME_SLOT) & (main_df['Timestamp'] < (k + 1) * TIME_SLOT)
    period_df = main_df[time_filter]

    # Calculate man-hours for each operation within the period
    man_hours = 0
    for op_id in period_df['Operation ID'].unique():
        operation_df = period_df[period_df['Operation ID'] == op_id]

        # Determine start time
        start_time = operation_df[operation_df['Start/End'] == 'start']['Timestamp'].min()
        if pd.isna(start_time):
            start_time = k * TIME_SLOT
        
        # Determine end time
        end_time = operation_df[operation_df['Start/End'] == 'end']['Timestamp'].max()
        if pd.isna(end_time):
            end_time = (k + 1) * TIME_SLOT
        
        # Count total interactions and calculate man-hours
        heads = len(operation_df['Interaction'])
        man_hours += heads * (end_time - start_time)

    daily_hours.append(man_hours)

# Results
daily_hours