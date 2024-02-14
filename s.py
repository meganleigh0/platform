import pandas as pd
import matplotlib.pyplot as plt

# Assuming your DataFrame is named operations_df
# Replace 'your_dataframe.csv' with your actual CSV file if you're reading from a CSV
# operations_df = pd.read_csv('your_dataframe.csv')

# Summarize data
print("Unique stations:", operations_df['station'].nunique())
print("Unique departments:", operations_df['department'].nunique())
print("Unique assemblies:", operations_df['assembly_description'].nunique())

# Group data by 'station' and get unique assemblies and operations
station_summary = operations_df.groupby('station').agg({
    'assembly_description': lambda x: x.nunique(),
    'description': lambda x: x.nunique(),
    'department': lambda x: x.nunique()
}).reset_index()

print("\nStation Summary:\n", station_summary)

# Analyze assemblies
assembly_summary = operations_df.groupby(['assembly_description', 'department']).agg({
    'description': lambda x: x.nunique(),
    'hours': 'sum'
}).reset_index()

print("\nAssembly Summary:\n", assembly_summary)

# Visualization: Number of operations per assembly
operations_per_assembly = operations_df.groupby('assembly_description')['description'].nunique()
operations_per_assembly.sort_values(ascending=False, inplace=True)

plt.figure(figsize=(10, 8))
operations_per_assembly.head(10).plot(kind='bar')  # Top 10 assemblies with the most operations
plt.title('Top 10 Assemblies by Number of Unique Operations')
plt.ylabel('Number of Operations')
plt.xlabel('Assembly Description')
plt.xticks(rotation=45)
plt.show()

# Visualization: Average hours spent on each assembly per department
hours_per_assembly_department = operations_df.groupby(['department', 'assembly_description'])['hours'].mean().unstack(fill_value=0)
plt.figure(figsize=(12, 10))
sns.heatmap(hours_per_assembly_department, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title('Average Hours Spent on Each Assembly Per Department')
plt.ylabel('Department')
plt.xlabel('Assembly Description')
plt.xticks(rotation=45)
plt.show()