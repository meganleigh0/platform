Coding for Zero and Non-Zero Differences
bar_fig = px.bar(
    df,
    x=df.index,
    y='Difference',
    color='Is_Aligned',  # Color based on whether the difference is zero or not
    text='Difference',
    hover_data=['WCAssigned', 'WorkCenter'],
    title='Difference between WCAssigned and WorkCenter with Zero Difference Highlighted'
)

# Customize labels and layout
bar_fig.update_layout(
    xaxis_title='Index',
    yaxis_title='Difference (Encoded Values)',
    coloraxis_colorbar=dict(
        title="Alignment"
    ),
    showlegend=True
)

# Show plot
bar_fig.show()

# Step 6: Print the DataFrame with the calculated differences
print(df[['WCAssigned', 'WorkCenter', 'WCAssigned_Num', 'WorkCenter_Num', 'Difference', 'Is_Aligned']])