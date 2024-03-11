import altair as alt
import pandas as pd

# Assuming all_operations is your DataFrame
# all_operations = pd.read_csv('your_dataframe.csv')  # Example to load your data

# 1. Longest Operations by Variant
chart1 = alt.Chart(all_operations).mark_bar().encode(
    x=alt.X('Variant:N', sort='-y'),
    y=alt.Y('max(Hours):Q', title='Max Hours per Operation'),
    color='Variant:N',
    tooltip=['Operation Description', 'max(Hours)']
).properties(title="Longest Operations by Variant")

# 2. Operation Similarities
chart2 = alt.Chart(all_operations).mark_circle().encode(
    x='Hours:Q',
    y='Variant:N',
    color='Variant:N',
    size='Hours:Q',
    tooltip=['Operation Description', 'Hours']
).properties(title="Operation Similarities Across Variants")

# 3. Station Workload
chart3 = alt.Chart(all_operations).mark_bar().encode(
    x='Station:N',
    y='sum(Hours):Q',
    color='Variant:N',
    tooltip=['Station', 'sum(Hours)']
).properties(title="Workload Distribution by Station")

# 4. Department Workload
chart4 = alt.Chart(all_operations).mark_bar().encode(
    x='Name:N',
    y='sum(TotalHours):Q',
    color='Variant:N',
    tooltip=['DepID', 'Name', 'sum(TotalHours)']
).properties(title="Workload Distribution by Department")

# 5. Part Number Repetitions
chart5 = alt.Chart(all_operations).mark_bar().encode(
    x='PartNumber:N',
    y='count(PartNumber):Q',
    color='Variant:N',
    tooltip=['PartNumber', 'count(PartNumber)']
).properties(title="Frequency of Part Numbers in Operations")

# Combine charts if needed, for example:
chart1 | chart2 | chart3 | chart4 | chart5

# Note: Due to the complexity and specificity of your request, some adjustments may be needed to fit your data structure and analysis goals.