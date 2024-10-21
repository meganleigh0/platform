import plotly.graph_objects as go
import plotly.express as px

# Group by ActionCategory for Hours and Count
df2 = df.groupby(['ActionCategory']).agg({"Hours": "sum", "ActionCategory": "count"}).rename(columns={"ActionCategory": "Count"})
df2 = df2.round(1)

# Doughnut chart for total hours
fig = go.Figure()

# Add doughnut chart for Hours
fig.add_trace(go.Pie(labels=df2.index, 
                     values=df2['Hours'], 
                     hole=.4, 
                     hoverinfo="label+percent+value", 
                     textinfo='label+value', 
                     name="Total Hours"))

# Update layout for the doughnut chart
fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(title_text="Assembly Hours by Action Category (Doughnut Chart)",
                  annotations=[dict(text='Hours', x=0.5, y=0.5, font_size=20, showarrow=False)],
                  height=500, width=500)

# Create a bar chart for the counts
fig2 = px.bar(df2, x=df2.index, y='Count', title="Action Category Count", text='Count')

# Update layout for bar chart
fig2.update_layout(height=300, width=500, yaxis_title="Count")

# Show both figures
fig.show()
fig2.show()