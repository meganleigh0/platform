import pandas as pd

def calculate_daily_hours(main_df, end):
    daily_hours = []
    for k in range(int(end//8) + 1):
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]
        period_df = period_df.sort_values(['Operation ID', 'Timestamp'])

        heads_list = []
        for ops in period_df['Operation ID'].unique():
            ops_df = period_df[period_df['Operation ID'] == ops]
            start_time = ops_df[ops_df['Start/End'] == 'start']['Timestamp'].values[0] if not ops_df[ops_df['Start/End'] == 'start'].empty else 8*k
            end_time = ops_df[ops_df['Start/End'] == 'end']['Timestamp'].values[0] if not ops_df[ops_df['Start/End'] == 'end'].empty else 8*(k+1)
            heads = len(ops_df['Interaction'].values[0])
            heads_list.append(heads * (end_time - start_time))
        daily_hours.append(sum(heads_list))
    return daily_hours

def track_vehicle_completions(log_df):
    completed_count = {}
    for month in range(20):
        month_df = log_df[(log_df['Timestamp'] < (month+1) * 160) & (log_df['Timestamp'] > month * 160)]
        month_df = month_df[month_df['Assembly'].isin(['prep and ship', 'prep ship']) & (month_df['Interaction'] == 'end')]

        for _, row in month_df.iterrows():
            vehicle_type = row['Vehicle'].split(':')[0]
            if vehicle_type not in completed_count:
                completed_count[vehicle_type] = [0] * 20  # Initialize list for each vehicle type
            completed_count[vehicle_type][month] += 1

        # Accumulate the count from previous months
        if month != 0:
            for vehicle in completed_count:
                completed_count[vehicle][month] += completed_count[vehicle][month - 1]

    return pd.DataFrame(completed_count)

# Example Usage
dept_logger = pd.DataFrame()  # Replace with actual DataFrame loading
assembly_logger = pd.DataFrame()  # Replace with actual DataFrame loading
daily_hours = calculate_daily_hours(dept_logger, 160)  # Assuming 'end' is 160
completed_vehicles = track_vehicle_completions(assembly_logger)
