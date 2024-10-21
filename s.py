import altair as alt
import pandas as pd

# Assuming your DataFrame `df` is available
# Group the data by 'ActionCategory' and calculate total hours and count for each
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Bar chart for Action Category Counts
bar_chart = alt.Chart(df2).mark_bar().encode(
    x=alt.X('ActionCategory:N', title="Action Category"),
    y=alt.Y('Count:Q', title="Count"),
    color=alt.Color('ActionCategory:N', legend=None),
    tooltip=['ActionCategory:N', 'Count:Q']
).properties(
    title="Action Category Count",
    width=300,
    height=300
)

# Simulated Doughnut chart using a Pie chart
# In Altair, we can use 'mark_arc' for pie chart and set an inner radius to simulate a doughnut
doughnut_chart = alt.Chart(df2).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Hours", type="quantitative", title="Total Hours"),
    color=alt.Color('ActionCategory:N', title="Action Category"),
    tooltip=['ActionCategory:N', 'Hours:Q']
).properties(
    title="Total Hours by Action Category",
    width=300,
    height=300
)

# Concatenate the bar chart and doughnut chart
final_chart = alt.hconcat(doughnut_chart, bar_chart)

# Display the chart
final_chart.display()
