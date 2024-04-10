import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Sample data with mixed date formats
data = {
    'Vehicle Number': [1, 2, 3, 4, 5],
    'Promise Date': ['2023-05-01', (2023, 5, 2), '2023-05-03', datetime(2023, 5, 4), '2023-05-05'],
    'Ship Date': [(2023, 5, 1), '2023-05-02', datetime(2023, 5, 3), '2023-05-04', '2023-05-06']
}

# Convert to DataFrame
df = pd.DataFrame(data)

def convert_to_datetime(date):
    if isinstance(date, tuple):
        return datetime(*date)
    elif isinstance(date, datetime):
        return date
    elif isinstance(date, str):
        try:
            return datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            pass
    # Add more conditions if there are more formats
    return pd.NaT  # Not a Time for unhandled formats

# Apply the conversion function to the date columns
df['Promise Date'] = df['Promise Date'].apply(convert_to_datetime)
df['Ship Date'] = df['Ship Date'].apply(convert_to_datetime)

# Calculate on-time performance
df['On Time'] = df['Ship Date'] <= df['Promise Date']

# Count the number of on-time and delayed vehicles
summary = df['On Time'].value_counts()

# Visualize the results
plt.figure(figsize=(8, 5))
summary.plot(kind='bar')
plt.title('On-time vs. Delayed Shipments')
plt.xlabel('On Time')
plt.ylabel('Number of Vehicles')
plt.xticks([0, 1], ['On Time', 'Delayed'], rotation=0)
plt.show()