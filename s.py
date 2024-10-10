whether the difference is zero or not
df['Movement'] = np.where(df['Difference'] > 0, 'Movement', 'No Movement')

# Step 5: Group by WCAssigned and count how many movements and no movements per work center
movement_summary = df.groupby(['WCAssigned', 'Movement']).size().unstack(fill_value=0)

# Step 6: Visualize the number of movements per work center
movement_fig = movement_summary.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6),
    title="Number of Movements and No Movements per Work Center",
    ylabel="Number of Operations"
)

# Step 7: Show the plot
plt.show()

# Step 8: Print the movement summary for reference
print(movement_summary)