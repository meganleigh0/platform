
# Define the correct order for months
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Convert the MONTH column to a categorical type with the correct order
df['MONTH'] = pd.Categorical(df['MONTH'], categories=month_order, ordered=True)

# Group by YEAR, MONTH, STATUS, FAMILY, and sum the QUANTITY
df_grouped = df.groupby(['YEAR', 'MONTH', 'STATUS', 'FAMILY'], as_index=False)['QUANTITY'].sum()

# Create the bar plot using Plotly, now colored by 'FAMILY' and sorted by MONTH
fig = px.bar(df_grouped, 
             x='MONTH', 
             y='QUANTITY', 
             color='FAMILY',  # Color by family
             barmode='stack', 
             facet_col='YEAR', 
             title="Sum of Quantities by Month, Family, and Status",
             hover_data=['STATUS'])  # Show status on hover

# Display the plot
fig.show()