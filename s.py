import pandas as pd

def calculate_daily_headcount(dept_logger, num_months):
    main_df = pd.DataFrame(dept_logger.log)
    daily_heads = []
    end = num_months * 160  # based on number of months and hours per month

    for k in range(int(end // 8)):
        period_heads = {}
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]

        # Iterate over each row to gather interactions by department
        for _, row in period_df.iterrows():
            department = row['Department']
            interactions = row['Interaction']  # Assuming this is a list of hashable items
            if department not in period_heads:
                period_heads[department] = set()
            # Flatten and add each unique interaction
            period_heads[department].update(interactions)

        # Calculate headcount per department and aggregate for the period
        daily_headcount = 0
        for department, interactions in period_heads.items():
            headcount = 8 * len(interactions)  # Each unique interaction counted as 8 man-hours
            daily_headcount += headcount

        daily_heads.append(daily_headcount)

    return daily_heads

# Example usage
dept_logger = pd.DataFrame()  # Replace with your actual DataFrame loading
num_months = 20
daily_headcounts = calculate_daily_headcount(dept_logger, num_months)
