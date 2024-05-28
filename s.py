def calculate_daily_headcount(dept_logger, num_months):
    main_df = pd.DataFrame(dept_logger.log)
    end = num_months * 160  # Calculate the end based on number of months and hours per month
    daily_headcounts = {}

    # Initialize the dictionary for each department
    unique_departments = main_df['Department'].unique()
    for department in unique_departments:
        daily_headcounts[department] = [0] * (end // 8)

    for k in range(int(end // 8)):
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]
        period_heads = {dept: set() for dept in unique_departments}

        # Aggregate unique interactions by department for this period
        for _, row in period_df.iterrows():
            department = row['Department']
            interaction = row['Interaction']  # Assuming this is directly hashable
            period_heads[department].add(interaction)

        # Update daily headcounts for each department for this period
        for department in unique_departments:
            daily_headcounts[department][k] = 8 * len(period_heads[department])  # Compute man-hours

    return daily_headcounts
