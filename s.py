import pandas as pd

def initialize_dataframe(log_data):
    """ Initialize and sort the DataFrame from log data. """
    df = pd.DataFrame(log_data)
    return df.sort_values(['Operation ID', 'Timestamp'])

def filter_dataframe_for_period(df, period, time_slot):
    """ Filter DataFrame for the given period based on the time slot. """
    start_time = period * time_slot
    end_time = (period + 1) * time_slot
    return df[(df['Timestamp'] >= start_time) & (df['Timestamp'] < end_time)]

def calculate_man_hours(df, period, time_slot):
    """ Calculate total man-hours for the given period DataFrame. """
    man_hours = 0
    for op_id in df['Operation ID'].unique():
        operation_df = df[df['Operation ID'] == op_id]
        start_time = operation_df[operation_df['Start/End'] == 'start']['Timestamp'].min()
        end_time = operation_df[operation_df['Start/End'] == 'end']['Timestamp'].max()
        
        if pd.isna(start_time):
            start_time = period * time_slot
        if pd.isna(end_time):
            end_time = (period + 1) * time_slot

        heads = len(operation_df['Interaction'])
        man_hours += heads * (end_time - start_time)
    return man_hours

def compute_daily_hours(log_data, end, time_slot=8):
    """ Compute daily man-hours from log data. """
    df = initialize_dataframe(log_data)
    total_periods = int(end // time_slot) + 1
    daily_hours = []
    
    for period in range(total_periods):
        period_df = filter_dataframe_for_period(df, period, time_slot)
        period_man_hours = calculate_man_hours(period_df, period, time_slot)
        daily_hours.append(period_man_hours)
    
    return daily_hours

# Example usage
dept_logger_log = [...]  # Placeholder for actual log data
end = 160  # Example end time
daily_hours = compute_daily_hours(dept_logger_log, end)
print(daily_hours)
