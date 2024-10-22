import altair as alt
import pandas as pd

# Assuming `top_ten_max` is already your DataFrame with the top 10 rows
# Example DataFrame (replace with your own)
top_ten_max = pd.DataFrame({
    'WCAssigned': ['Operator 14 - 1', 'Operator 4 & 5 - SUBS', 'Operator 13 - 1', ...],  # Replace ... with actual values
    'Critical_Path_End_Time': [25, 23, 22, ...],  # Replace with actual values
    'Program': ['Program A', 'Program B', 'Program A', ...],  # Replace with actual values
    'Operator_Max_Critical_Path': [25, 23, 22, ...],  # Replace with actual values
    'WC_Hours': [40, 38, 37, ...]  # Replace with actual values
})

# Create the bar chart
bars = alt.Chart(top_ten_max).mark_bar().encode(
    x=alt.X('WCAssigned', title='Work Center'),
    y=alt.Y('Critical_Path_End_Time', title='Critical Path End Time (hours)'),
    color='Program',
    tooltip=['WCAssigned', 'Critical_Path_End_Time', 'WC_Hours']
).properties(
    title="Top 10 Critical Path Work Centers by Program"
)

# Add annotations for the top 3 maximum values
annotations = alt.Chart(top_ten_max).mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to the right
).encode(
    x='WCAssigned',
    y='Critical_Path_End_Time',
    text=alt.condition(
        alt.datum.Critical_Path_End_Time.isin(sorted(top_ten_max['Critical_Path_End_Time'], reverse=True)[:3]), 
        alt.value('MAX'), 
        alt.value('')
    )
)

# Combine the bars and annotations
chart = bars + annotations

# Display the chart
chart.configure_axis(
    labelAngle=0
).configure_title(
    fontSize=16
).configure_legend(
    titleFontSize=12,
    labelFontSize=10
)