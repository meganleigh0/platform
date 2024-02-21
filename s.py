import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Example data
data = {
    'station': ['Station A', 'Station B', 'Station C', 'Station D'],
    'assembly_count': [100, 150, 200, 120],
    'operation_count': [80, 160, 140, 130],
    'departments': ['Dept 1', 'Dept 2', 'Dept 3', 'Dept 1']
}
df = pd.DataFrame(data)

# Bar Chart for Assembly and Operation Counts by Station
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(df['station']))

plt.bar(index, df['assembly_count'], bar_width, label='Assembly Count')
plt.bar([i+bar_width for i in index], df['operation_count'], bar_width, label='Operation Count')

plt.xlabel('Station')
plt.ylabel('Counts')
plt.title('Assembly and Operation Counts by Station')
plt.xticks([i + bar_width / 2 for i in index], df['station'])
plt.legend()
plt.tight_layout()
plt.show()

# Convert departments to a categorical type for better color mapping
df['departments'] = pd.Categorical(df['departments'])

# Heatmap for Assembly and Operation Counts by Department (Mockup, needs pivot data)
# This is an illustrative step, assuming departments and stations are related in a matrix form
# For a real heatmap, we would need a pivot table or correlation matrix here

# Pair Plot (Scatterplot Matrix) example
sns.pairplot(df, hue='departments')
plt.show()