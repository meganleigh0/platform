import pandas as pd

# Sample dataframe creation (replace this with your actual dataframe)
data = {
    'Code': ['A1', 'A2', 'A3', 'A4'],
    'Year': [2021, 2021, 2022, 2022],
    'Month': ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']  # Adjust your actual month columns here
}

df = pd.DataFrame(data)

# Define the correct month mapping based on position
months_full = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Group by 'Year' or handle year-wise, assuming 12 month values for each year
df['Month_full'] = df.groupby('Year').apply(lambda x: months_full[:len(x)]).explode().reset_index(drop=True)

# This will now map the month letters to their full names in order for each year
print(df)