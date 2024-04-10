import pandas as pd
import matplotlib.pyplot as plt

# Assuming df is your DataFrame after the previous operations

# Extract the month from the Ship Date
df['Ship Month'] = df['Ship Date'].dt.month

# Group by the extracted month and count the number of vehicles
monthly_shipments = df.groupby('Ship Month')['Vehicle Number'].count()

# Visualize the results
plt.figure(figsize=(10, 6))
monthly_shipments.plot(kind='bar')
plt.title('Number of Vehicles Shipped Each Month')
plt.xlabel('Month')
plt.ylabel('Number of Vehicles')
plt.xticks(rotation=0)
plt.show()