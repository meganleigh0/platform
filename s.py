# Group by YEAR, MONTH, and STATUS, and sum the QUANTITY
df_grouped = df.groupby(['YEAR', 'MONTH', 'STATUS'], as_index=False)['QUANTITY'].sum()

# Create the bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='MONTH', y='QUANTITY', hue='STATUS', data=df_grouped, ci=None)

# Customize the plot
plt.title('Sum of Quantities by Month and Status (2022-2028)')
plt.xlabel('Month')
plt.ylabel('Total Quantity')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Display the plot
plt.tight_layout()
plt.show()