import pandas as pd

def extract_vehicles_and_summary(df):
    # Reset index for easier manipulation
    df.reset_index(drop=True, inplace=True)
    
    # Assume 'Armor In' column indicates where station summaries might be restarting
    # Find indices where 'Armor In' is not NaN which implies the start of a new block
    starts = df[df['Armor In'].notna()].index.tolist()
    
    # Assuming the end of one block and start of the next is continuous
    ends = starts[1:] + [len(df)]  # Add the end of the DataFrame as the end of the last block

    summary_list = []
    vehicle_list = []
    
    for start, end in zip(starts, ends):
        block = df.iloc[start:end].copy()
        block.dropna(how='all', axis=1, inplace=True)  # Drop columns where all entries are NaN
        
        # Find the 'Total' row as the summary separator
        total_index = block[block.apply(lambda x: 'Total' in x.values, axis=1)].index[0]
        
        # Summary information
        summary_df = block.iloc[:total_index + 1]
        summary_df['Station'] = df.iloc[start]['Armor In']  # Station name from 'Armor In'
        summary_list.append(summary_df)
        
        # Vehicle information
        vehicle_df = block.iloc[total_index + 1:]
        vehicle_df['Station'] = df.iloc[start]['Armor In']  # Station name from 'Armor In'
        vehicle_list.append(vehicle_df)
        
    # Concatenate all blocks into two separate DataFrames
    all_summary_df = pd.concat(summary_list).reset_index(drop=True)
    all_vehicle_df = pd.concat(vehicle_list).reset_index(drop=True)
    
    return all_summary_df, all_vehicle_df

# Usage example
summary_data, vehicle_data = extract_vehicles_and_summary(data)

# Display the extracted data
print("Summary Data:")
print(summary_data)
print("\nVehicle Data:")
print(vehicle_data)