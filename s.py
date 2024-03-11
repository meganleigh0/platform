import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style for seaborn
sns.set(style="whitegrid")

# 1. Distribution of Hours per Operation
plt.figure(figsize=(10, 6))
sns.histplot(all_operations_df['Hours'], bins=30, kde=True)
plt.title('Distribution of Hours Spent per Operation')
plt.xlabel('Hours')
plt.ylabel('Frequency')
plt.show()

# 2. Top Operations by Total Hours
# Aggregating hours by operation description
operation_hours_sum = all_operations_df.groupby('Operation Description')['Hours'].sum().nlargest(10)
plt.figure(figsize=(10, 6))
operation_hours_sum.plot(kind='bar')
plt.title('Top 10 Operations by Total Hours')
plt.xlabel('Operation Description')
plt.ylabel('Total Hours')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 3. Department Involvement in Operations
# Aggregating counts of operations by department
department_operations_count = all_operations_df['Name'].value_counts().head(10)
plt.figure(figsize=(10, 8))
department_operations_count.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Departments Involved in Operations')
plt.ylabel('')  # Hide y-label for cleaner look
plt.tight_layout()
plt.show()