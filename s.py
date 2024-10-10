import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Example DataFrame (Replace this with your actual data)
data = {
    'WCAssigned': ['400A', '400B', '4001', '4002', '4003', '400A', '4002'],
    'WorkCenter': ['400A', '400B', '4003', '4002', '4001', '4002', '400B']
}
df = pd.DataFrame(data)

# Step 1: Create a mapping of the WorkCenters to numerical values
unique_workcenters = sorted(set(df['WCAssigned'].unique()).union(df['WorkCenter'].unique()))
workcenter_map = {center: i for i, center in enumerate(unique_workcenters)}

# Step 2: Encode the WCAssigned and WorkCenter columns to numerical values
df['WCAssigned_Num'] = df['WCAssigned'].map(workcenter_map)
df['WorkCenter_Num'] = df['WorkCenter'].map(workcenter_map)

# Step 3: Calculate the absolute difference between the two columns
df['Difference'] = np.abs(df['WCAssigned_Num'] - df['WorkCenter_Num'])

# Step 4: Visualize the differences

# 4.1 Scatter Plot of WCAssigned vs WorkCenter
plt.figure(figsize=(10,6))
plt.scatter(df['WCAssigned_Num'], df['WorkCenter_Num'], c=df['Difference'], cmap='viridis', s=100)
plt.colorbar(label='Difference Magnitude')
plt.title('WCAssigned vs WorkCenter')
plt.xlabel('WCAssigned (Encoded)')
plt.ylabel('WorkCenter (Encoded)')
plt.show()

# 4.2 Bar Chart Showing the Differences
plt.figure(figsize=(10,6))
plt.bar(df.index, df['Difference'], color='blue')
plt.title('Difference between WCAssigned and WorkCenter')
plt.xlabel('Index')
plt.ylabel('Difference (Encoded Values)')
plt.show()

# Step 5: Print the DataFrame with the calculated differences
print(df[['WCAssigned', 'WorkCenter', 'WCAssigned_Num', 'WorkCenter_Num', 'Difference']])


	1.	Numerical Encoding: Since the values like 400A, 400B, etc., are categorical but ordered, we first encode them into numerical values based on their position in the sorted list of unique work center values. This helps us quantify their differences.
	2.	Difference Calculation: Once the WCAssigned and WorkCenter values are converted to numbers, we calculate the absolute difference between these numerical representations for each row. A smaller difference indicates that the two columns are closely aligned for that entry, while a larger difference indicates a bigger deviation.
	3.	Visualizations:
	•	Scatter Plot: This plot shows WCAssigned vs WorkCenter, where the color intensity represents the magnitude of the difference between the two columns. It’s useful for identifying patterns in differences visually.
	•	Bar Chart: The bar chart shows the magnitude of differences for each row. This helps quantify and easily compare the differences across the entire dataset.

This analysis helps you understand how “different” the WCAssigned and WorkCenter values are by assigning numerical values based on their order and visually presenting the magnitude of the differences.
