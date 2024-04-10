import pandas as pd
import matplotlib.pyplot as plt

# Assuming status is your dictionary with program names as keys and DataFrames as values

# Initialize an empty list to store the processed DataFrames
processed_data = []

# Iterate through each program in the dictionary
for program_name, df in status.items():
    # Copy the DataFrame to avoid modifying the original
    temp_df = df.copy()
    
    # Add a column for the program name
    temp_df['Program'] = program_name
    
    # Create a column combining year and month from the Ship Date
    temp_df['Year-Month'] = temp_df['Ship Date'].dt.to_period('M')
    
    # Group by the new Year-Month column and count the number of vehicles
    monthly_data = temp_df.groupby(['Year-Month', 'Program'])['Vehicle Number'].count().reset_index()
    
    # Add the processed data to the list
    processed_data.append(monthly_data)

# Concatenate all the processed DataFrames into one
combined_data = pd.concat(processed_data)

# Pivot the data for the stacked bar chart
pivot_data = combined_data.pivot(index='Year-Month', columns='Program', values='Vehicle Number')

# Plot the stacked bar chart
pivot_data.plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Number of Vehicles Shipped Each Month and Year by Program')
plt.xlabel('Month and Year')
plt.ylabel('Number of Vehicles')
plt.xticks(rotation=45)
plt.legend(title='Program')
plt.show()