def calculate_hours_by_station_optimized(df):
    # Explode the 'operations' column to separate rows
    exploded_df = df.explode('operations')

    # Calculate hours for each row
    exploded_df['hours'] = exploded_df['operations'].apply(lambda op: float(op[0]))

    # Group by 'station' and sum the hours
    station_hours = exploded_df.groupby('station')['hours'].sum()

    return station_hours.to_dict()
