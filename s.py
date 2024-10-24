

import pandas as pd
import plotly.express as px

# Example DataFrame (adjust with your actual data)
data = {
    'YEAR': [2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023],
    'MONTH': ['Jan', 'Feb', 'Mar', 'Apr', 'Jan', 'Feb', 'Mar', 'Apr'],
    'QUANTITY': [100, 150, 120, 130, 200, 250, 220, 230],
    'STATUS': ['Active', 'Inactive', 'Active', 'Active', 'Inactive', 'Active', 'Inactive', 'Inactive']
}

df = pd.DataFrame(data)

# Group by YEAR, MONTH, and STATUS, and sum the QUANTITY
df_grouped = df.groupby(['YEAR', 'MONTH', 'STATUS'], as_index=False)['QUANTITY'].sum()

# Create the bar plot using Plotly
fig = px.bar(df_grouped, x='MONTH', y='QUANTITY', color='STATUS', barmode='stack',
             facet_col='YEAR', title="Sum of Quantities by Month and Status")

# Display the plot
fig.show()