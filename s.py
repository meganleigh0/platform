import pandas as pd

# Example DataFrame
data = {
    'YEAR': [2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022,
             2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
    'MONTH': ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D',
              'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
}

df = pd.DataFrame(data)

# Define the correct month sequence pattern
correct_month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Initialize a counter to keep track of the position in the month sequence
current_position = 0

# Helper function to map the current position to the correct month
def map_to_correct_month(index):
    global current_position
    # Map the current position to the correct month in the sequence
    correct_month = correct_month_order[current_position % 12]
    # Increment the position to move to the next month in the sequence
    current_position += 1
    return correct_month

# Apply the pattern matching function to assign the correct month
df['UNIQUE_MONTH'] = df.index.map(map_to_correct_month)

# Display the updated DataFrame
import ace_tools as tools; tools.display_dataframe_to_user(name="Mapped Month Data", dataframe=df)