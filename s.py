import pandas as pd

# Example DataFrame
data = {
    'YEAR': [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022,
             2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
    'MONTH': ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
              'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
}

df = pd.DataFrame(data)

# Define the full list of months in the correct order
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Track which months have been assigned
assigned_months = []

# Helper function to assign the correct month based on the order in the data
def assign_month(index, month_abbreviation):
    # Check if the abbreviation is 'J', 'M', or 'A' which can represent multiple months
    if month_abbreviation == 'J':
        # Assign either January or July based on what has already been assigned
        return 'Jan' if 'Jan' not in assigned_months else 'Jul'
    elif month_abbreviation == 'M':
        # Assign either March or May based on what has already been assigned
        return 'Mar' if 'Mar' not in assigned_months else 'May'
    elif month_abbreviation == 'A':
        # Assign either April or August based on what has already been assigned
        return 'Apr' if 'Apr' not in assigned_months else 'Aug'
    else:
        # For other abbreviations, use the month map
        month_map = {
            'F': 'Feb',
            'S': 'Sep',
            'O': 'Oct',
            'N': 'Nov',
            'D': 'Dec'
        }
        return month_map[month_abbreviation]

# Apply the month assignment logic to the DataFrame
df['UNIQUE_MONTH'] = df.apply(lambda row: assign_month(row.name, row['MONTH']), axis=1)

# Ensure that the month is added to the assigned_months list
df['UNIQUE_MONTH'].apply(lambda x: assigned_months.append(x))

# Show the updated DataFrame
import ace_tools as tools; tools.display_dataframe_to_user(name="Updated Month Data", dataframe=df)