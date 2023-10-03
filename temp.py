import pandas as pd

# Load the necessary data frames
standards = pd.read_csv('standards.csv')
dep_df = pd.read_csv('dep_data.csv')

# Load variant data frames dynamically, replace these lines with actual loading mechanism
variant_dfs = {var: pd.read_csv(f'{var}_mbom.csv') for var in ['producta', 'productb', 'productc', 'productd', 'producte']}

# Initializing the dictionary to store variant parts with their total hours
variant_parts = {}

# Loop through each variant
for var, df in variant_dfs.items():
    # Filter rows where PartNumber in standards
    # and multiply each part's quantity by its listed hours in standards
    part_hours_list = []
    for index, row in df.iterrows():
        part_no = row['PartNumber']
        qty = row['Qty']
        # Filtering standards for each part
        part_standards = standards[standards['PlanNo'] == part_no]
        # Calculating effective time for each operation, summing, and appending
        for _, operation in part_standards.iterrows():
            dep_efficiency = dep_df[dep_df['DepID'] == operation['Department']]['Efficiency'].values[0]
            effective_time = operation['Hours'] / dep_efficiency  # You can adjust this calculation
            part_hours_list.append((operation['Department'], effective_time * qty))
    
    # Convert list of tuples to DataFrame
    part_hours_df = pd.DataFrame(part_hours_list, columns=['Department', 'Hours'])
    # Sum the hours for each department
    department_hours = part_hours_df.groupby('Department')['Hours'].sum().reset_index()
    variant_parts[var] = department_hours



import plotly.express as px

# Step 1: Calculate Capacity for Each Department and Variant
for var, df in variant_parts.items():
    # Merge with dep_df to get Available Hours and Efficiency for each department
    merged_df = pd.merge(df, dep_df, left_on='Department', right_on='DepID', how='left')
    # Calculate the Capacity for each Department
    merged_df['Capacity'] = merged_df['Available Hours'] * merged_df['Efficiency'] / merged_df['Hours']
    variant_parts[var] = merged_df  # Update the df in variant_parts dictionary

# Step 2: Graph Department Capacity
for var, df in variant_parts.items():
    # Bar Plot for Each Variant's Department Capacity
    fig = px.bar(df, x='Department', y='Capacity', title=f'{var} - Department Capacity',
                 labels={'Capacity': 'Capacity', 'Department': 'Department'})
    fig.show()

# Step 3: Aggregate Department Hours by Plant for Each Variant
# This step assumes your dep_df has a 'Plant' column mapping each department to a plant
plant_capacity = {}
for var, df in variant_parts.items():
    # Merge with dep_df to get the 'Plant' for each department, then group by 'Plant'
    df_with_plant = pd.merge(df, dep_df[['DepID', 'Plant']], left_on='Department', right_on='DepID', how='left')
    plant_hours = df_with_plant.groupby('Plant')['Hours'].sum().reset_index()
    # Calculate Plant Capacity
    # This step might need to be adjusted based on how you calculate total available hours for a plant
    # For example, you might need to sum the available hours of all departments in a plant
    plant_hours['Capacity'] = plant_hours['Hours']  # Adjust this line with the correct calculation
    plant_capacity[var] = plant_hours

# Step 4: Graph Plant Capacity
for var, df in plant_capacity.items():
    # Bar Plot for Each Variant's Plant Capacity
    fig = px.bar(df, x='Plant', y='Capacity', title=f'{var} - Plant Capacity',
                 labels={'Capacity': 'Capacity', 'Plant': 'Plant'})
    fig.show()

