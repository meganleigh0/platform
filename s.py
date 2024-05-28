import pandas as pd

    
    # Convert Timestamp to hours and then to days by integer division
    main_df['Day'] = main_df['Timestamp'] // 8
    
    # Group by day and department, then aggregate interactions into sets
    grouped = main_df.groupby(['Day', 'Department'])['Interaction'].agg(set).reset_index()
    
    # Calculate headcount by multiplying the size of each set by 8 (man-hours per unique interaction)
    grouped['Headcount'] = grouped['Interaction'].apply(len) * 8
    
    # Sum up headcount per day across all departments
    daily_headcount = grouped.groupby('Day')['Headcount'].sum().tolist()
    
