import altair as alt
import pandas as pd

# Assuming you have df loaded
# Create the aggregate dataframe for Hours and Counts
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Bar chart for Action Category Counts
bar_chart = alt.Chart(df2).mark_bar().encode(
    x=alt.X('ActionCategory:N', title="Action Category"),
    y=alt.Y('Count:Q', title="Count"),
    color='ActionCategory:N',
    tooltip=['ActionCategory:N', 'Count:Q']
).properties(
    title="Action Category Count",
    width=300,
    height=300
)

# Simulate a doughnut chart (Altair uses layered arcs to simulate a pie chart)
doughnut_chart = alt.Chart(df2).mark_arc(innerRadius=50, outerRadius=100).encode(
    theta=alt.Theta('Hours:Q', title="Total Hours"),
    color=alt.Color('ActionCategory:N', legend=None),
    tooltip=['ActionCategory:N', 'Hours:Q']
).properties(
    title="Total Hours by Action Category",
    width=300,
    height=300
)

# Concatenate the bar chart and the doughnut chart
final_chart = alt.hconcat(doughnut_chart, bar_chart)

# Show the final chart
final_chart.display()
