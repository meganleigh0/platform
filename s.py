import altair as alt
import pandas as pd

# Assuming your DataFrame 'df' is available
# Group the data by 'ActionCategory' and calculate total hours and count for each
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Create a simple bar chart showing total Hours with the Count displayed as text labels
chart = alt.Chart(df2).mark_bar(size=40).encode(
    x=alt.X('ActionCategory:N', title="Action Category"),
    y=alt.Y('Hours:Q', title="Total Hours"),
    color=alt.Color('ActionCategory:N', legend=None),
    tooltip=['ActionCategory:N', 'Hours:Q', 'Count:Q']
).properties(
    title="Total Hours and Count by Action Category",
    width=500,
    height=300
).configure_axis(
    grid=False  # Remove grid lines for a cleaner look
).configure_view(
    strokeWidth=0  # Remove the chart border
).configure_title(
    fontSize=16,
    anchor='start',
    offset=10
)

# Add text labels for the Count on top of the bars
text = chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-5  # Move text slightly above the bars
).encode(
    text='Count:Q'  # Show count as labels
)

# Layer the bar chart and the text labels
final_chart = chart + text

# Display the chart
final_chart.display()