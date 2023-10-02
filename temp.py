# Set index for efficient lookup
dep_df.set_index('DepID', inplace=True)

# Function to adjust hours based on efficiency
def adjust_hours(row):
    dep_efficiency = dep_df.at[row['Department'], 'Efficiency']
    return row['Hours'] / dep_efficiency if dep_efficiency != 0 else 0

standards_df['AdjustedHours'] = standards_df.apply(adjust_hours, axis=1)

for index, row in mbom_df.iterrows():
    part = row['PartNumber']
    quantity = row['Qty']
    make_or_buy = row['Make/Buy']
    
    # Filter standards_df for rows related to the current part
    part_standards = standards_df[standards_df['PlanNo'] == part]
    
    # Sum the AdjustedHours for each Department
    part_hours = part_standards.groupby('Department')['AdjustedHours'].sum().reset_index()
    
    # If it's a 'Make' part, consider the quantity
    if make_or_buy == 'Make':
        part_hours['AdjustedHours'] *= quantity
    
    # Add PartNumber to the result
    part_hours['PartNumber'] = part
    
    # Concatenate the result to final_result
    final_result = pd.concat([final_result, part_hours], ignore_index=True)
