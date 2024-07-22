import pandas as pd

def process_station_data(df):
    """
    Process station data to extract and organize vehicle and program details.
    
    Args:
    df (pd.DataFrame): DataFrame containing data for a specific section.
    
    Returns:
    pd.DataFrame: Processed DataFrame with structured vehicle and program data.
    """
    # Drop any completely empty rows and columns
    df = df.dropna(how='all').dropna(how='all', axis=1)

    # Define a new DataFrame to hold the structured data
    structured_data = pd.DataFrame()

    # Iterate over the DataFrame rows
    for idx, row in df.iterrows():
        # Check if row contains vehicle and program data based on expected format (e.g., contains VIN or identifier like 'A90')
        if any(row.str.contains('A90|P20|S40|Y30', regex=True, na=False)):
            # Extract and process the data
            for item in row.dropna():
                # Split the item into its components based on spaces (assuming format like '1234 P20 36')
                parts = item.split()
                if len(parts) >= 2:
                    vin = parts[0]
                    program = parts[1]
                    qty = int(parts[2]) if len(parts) == 3 else None  # Include quantity if present
                    # Append to the DataFrame
                    structured_data = structured_data.append({
                        'VIN': vin,
                        'Program': program,
                        'Quantity': qty
                    }, ignore_index=True)

    # If there are named columns for contract, MRP, etc., extract this information too
    if 'Contract' in df.columns:
        contract_data = df.loc[df['Contract'].notna(), ['Contract', 'MRP', 'Actual', 'Delta', 'Flow']]
        structured_data = pd.concat([structured_data, contract_data], axis=1)

    return structured_data

# Example usage:
# Assuming you have a DataFrame 'teardown_data' from the 'Teardown' section
# processed_data = process_station_data(teardown_data)
# print(processed_data)