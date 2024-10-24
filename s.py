# Define the correct month mapping based on position
months_full = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Since the month letters are in order, we can apply the mapping in sequence
def map_months_to_full_name(month_series):
    return pd.Series(months_full[:len(month_series)], index=month_series.index)

# Apply the mapping to the 'Month' column for each year
df['Month_full'] = df.groupby('Year')['Month'].apply(map_months_to_full_name)

# Display the updated dataframe
print(df)