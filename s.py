# Step 1: Select the relevant quantity columns
# Assuming your quantity columns are from Q1 to Q4 of each year or specific month columns
quantity_columns = ['Q1_2015', 'Q2_2015', 'Q3_2015', 'Q4_2015', 'Q1_2016', 'Q2_2016']  # Adjust based on your columns

# Step 2: Filter out programs where the sum of quantities across all columns is zero
filtered_df = df[df[quantity_columns].sum(axis=1) != 0]

# Step 3: If you want to group by 'Program' and remove programs where all quantities are zero
grouped_filtered_df = filtered_df.groupby('Program').filter(lambda x: x[quantity_columns].sum().sum() != 0)

# 'grouped_filtered_df' now contains only programs with at least one non-zero quantity.