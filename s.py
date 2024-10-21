import altair as alt
import pandas as pd

# Assuming your DataFrame 'df' is available
# Group the data by 'ActionCategory' and calculate total hours and count for each
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Create a simple bar chart showing total Hours
chart = alt.Chart(df2).mark_bar(size=40).encode(
    x=alt.X('ActionCategory:N', title="Action Category"),
    y=alt.Y('Hours:Q', title="Total Hours"),
    color=alt.Color('ActionCategory:N', legend=None),  # Remove the legend for simplicity
    tooltip=['ActionCategory:N', 'Hours:Q', 'Count:Q']
).properties(
    title="Total Hours and Count by Action Category",
    width=500,
    height=300
)

# Add text labels for the Count on top of the bars
text = chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-5  # Move text slightly above the bars
).encode(
    text='Count:Q'  # Show count as labels
)

# Display the final chart with the text layered on top
final_chart = chart + text

# Display the final chart
final_chart.display()