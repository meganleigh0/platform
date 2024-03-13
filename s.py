import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'mbom_df' is your DataFrame

# Step 2: Aggregate the data
aggregated_data = mbom_df.groupby(['Usr Org', 'Sec Org', 'Make/Buy'])['PartNumber'].count().reset_index(name='Count')

# Step 3: Visualization
# Creating a pivot table for the aggregated data
pivot_table = aggregated_data.pivot_table(index=['Usr Org', 'Sec Org'], columns='Make/Buy', values='Count', fill_value=0).reset_index()

# Plotting
plt.figure(figsize=(12, 8))
sns.barplot(x='Sec Org', y='Count', hue='Make/Buy', data=aggregated_data, palette=['#4C9F70', '#F44336'])
plt.title('Make vs Buy Counts per Sec Org and Usr Org')
plt.xlabel('Sec Org')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Make/Buy')
plt.tight_layout()

plt.show()