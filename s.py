# Filtering starting and ending points
start_df = df[df['Interaction'].str.contains('Starting')].rename(columns={'Timestamp': 'Start_Time'})
end_df = df[df['Interaction'].str.contains('finish')].rename(columns={'Timestamp': 'End_Time'})

# Merging the dataframes on AssemblyID to get start and end times in the same row
merged_df = pd.merge(start_df, end_df, on=['AssemblyID', 'Vehicle', 'Section'], how='left')
fig = px.line(merged_df, x='Start_Time', x_end='End_Time', y='AssemblyID', y_end='AssemblyID', color='Vehicle', facet_col='Section', title="Assembly over time")

fig.show()