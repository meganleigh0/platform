import altair as alt
import pandas as pd

# Assuming your DataFrame 'df' is available
# Group the data by 'ActionCategory' and calculate total hours and count for each
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Create a simple bar chart showing total Hours
chart = alt.Chart(df2).mark_bar(size=40).encode(
    x=alt.X('ActionCategory:N', title="Action Category", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    y=alt.Y('Hours:Q', title="Total Hours", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    color=alt.Color('ActionCategory:N', legend=None),  # Remove the legend for simplicity
    tooltip=['ActionCategory:N', 'Hours:Q', 'Count:Q']
).properties(
    title=alt.TitleParams(
        text="Total Hours and Count by Action Category",
        fontSize=18,
        anchor='start',
        offset=15
    ),
    width=600,
    height=400
)

# Add text labels for the Count on top of the bars
text = chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-5,  # Move text slightly above the bars
    fontSize=14,  # Increase font size for labels
    fontWeight='bold'  # Make the count labels bold
).encode(
    text='Count:Q'  # Show count as labels
)

# Display the final chart with the text layered on top
final_chart = (chart + text).configure_axis(
    grid=False  # Remove grid lines for a cleaner look
).configure_view(
    strokeWidth=0  # Remove the chart border
)

# Display the final chart
final_chart.display()