import altair as alt
import pandas as pd

# Assuming your DataFrame 'df' is available
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

# Create a pie chart first
pie_chart = alt.Chart(df2).mark_arc().encode(
    theta=alt.Theta(field="Hours", type="quantitative", title="Total Hours"),
    color=alt.Color('ActionCategory:N', title="Action Category"),
    tooltip=['ActionCategory:N', 'Hours:Q']
).properties(
    width=300,
    height=300
)

# Add a white circle in the middle to simulate a doughnut chart
inner_circle = alt.Chart(pd.DataFrame({'dummy': ['']})).mark_arc(color='white').encode(
    theta=alt.value(1),
    color=alt.value('white')
).properties(
    width=100,
    height=100
)

# Layer the pie chart and the inner white circle to create the doughnut effect
doughnut_chart = pie_chart + inner_circle

# Concatenate the doughnut chart and bar chart
final_chart = alt.hconcat(doughnut_chart, bar_chart)

# Display the final chart
final_chart.display()
