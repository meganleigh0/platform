import pandas as pd

# Hard-coded data based on the image
data = {
    'Month': ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
    'Working Days': [20, 19, 23, 20, 22, 21, 20, 23, 20, 21, 20, 20],
    'Weekends': [9, 8, 8, 10, 8, 8, 8, 8, 9, 9, 8, 10],
    'Holidays': [2, 1, 0, 0, 1, 1, 1, 0, 1, 1, 2, 1],
    'Total': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Display the DataFrame
import ace_tools as tools; tools