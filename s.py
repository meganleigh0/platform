def calculate_daily_headcount(dept_logger, num_months):
    main_df = pd.DataFrame(dept_logger.log)
    end = num_months * 160  # based on number of months and hours per month
    daily_headcounts = {}

    for k in range(int(end // 8)):
        period_heads = {}
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]

        # Gather interactions by department
        for _, row in period_df.iterrows():
            department = row['Department']
            interactions = row['Interaction']  # Assuming this is a list of hashable items
            if department not in period_heads:
                period_heads[department] = set()
            # Flatten and add each unique interaction
            period_heads[department].update(interactions)

        # Store headcount for each department for the period
        for department, interactions in period_heads.items():
            if department not in daily_headcounts:
                daily_headcounts[department] = []
            # Calculate headcount as 8 times the number of unique interactions
            daily_headcounts[department].append(8 * len(interactions))

    return daily_headcounts
