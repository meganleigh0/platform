import pandas as pd

def calculate_daily_headcount(dept_logger, num_months):
    # Convert log to DataFrame
    main_df = pd.DataFrame(dept_logger.log)
    
    # Convert Timestamp to hours and then to days by integer division
    main_df['Day'] = main_df['Timestamp'] // 8
    
    # Convert lists in 'Interaction' to tuples (which are hashable)
    main_df['Interaction'] = main_df['Interaction'].apply(tuple)
    
    # Group by day and department, then aggregate interactions into sets
    grouped = main_df.groupby(['Day', 'Department'])['Interaction'].agg(lambda x: set(x)).reset_index()
    
    # Calculate headcount by multiplying the size of each set by 8 (man-hours per unique interaction)
    grouped['Headcount'] = grouped['Interaction'].apply(len) * 8
    
    # Sum up headcount per day across all departments
    daily_headcount = grouped.groupby('Day')['Headcount'].sum().tolist()
    
    return daily_headcount
