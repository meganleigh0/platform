import pandas as pd

def extract_vehicles_and_summary(df):
    # Reset index for easier slicing and to ensure columns are properly aligned
    df.reset_index(drop=True, inplace=True)
    
    # Locate the index for the row that contains 'Total' which separates summary from vehicle data
    total_index = df[df.apply(lambda x: 'Total' in x.values, axis=1)].index[0]
    
    # Extract summary data, assuming 'Total' row is included in summary
    summary_df = df.iloc[:total_index+1]
    
    # Assuming the station name is in a column that sometimes has empty cells, fill forward
    if 'Unnamed: 0' in df.columns:
        df['Unnamed: 0'].ffill(inplace=True)
    
    # Extract vehicle data
    vehicle_df = df.iloc[total_index+1:]
    
    # Clean up the DataFrame by dropping empty rows and columns if they are all NaN
    vehicle_df.dropna(how='all', inplace=True)
    vehicle_df.dropna(axis=1, how='all', inplace=True)
    
    # Add station information from 'Unnamed: 0' which we assume holds the station names
    if 'Unnamed: 0' in df.columns:
        vehicle_df['Station'] = df['Unnamed: 0'].iloc[total_index+1:].ffill()
    
    # Ensure the summary table also includes the station name added as a new column
    summary_df['Station'] = df['Unnamed: 0'].ffill()

    # Optionally, clean and rename columns in both DataFrames here as needed
    
    return summary_df, vehicle_df

# Assuming 'data' is your DataFrame loaded from the Excel or other data source
summary_data, vehicle_data = extract_vehicles_and_summary(data)

# Display the data
print("Summary Data:")
print(summary_data)
print("\nVehicle Data:")
print(vehicle_data)