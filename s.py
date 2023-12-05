
# Creating an animated bar plot
fig = px.bar(df, 
             x="Timestamp", 
             y=["Turret_Completed", "Turret_Processing", "Hull_Completed", "Hull_Processing"],
             labels={"value": "Count", "variable": "Status"},
             animation_frame="Timestamp",
             range_y=[0, df[["Turret_Completed", "Turret_Processing", "Hull_Completed", "Hull_Processing"]].values.max() + 1]
)

fig.update_layout(title="Simulation Data: Turrets and Hulls Status Over Time",
                  xaxis_title="Timestamp",
                  yaxis_title="Count",
                  barmode='group')

# Running the figure in your local Python environment
fig.show()
