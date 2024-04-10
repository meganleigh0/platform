import pandas as pd
import matplotlib.pyplot as plt

# Assuming df is your DataFrame after the previous operations

# Create a column combining year and month from the Ship Date
df['Year-Month'] = df['Ship Date'].dt.to_period('M')

# Group by the new Year-Month column and count the number of vehicles
monthly_yearly_shipments = df.groupby('Year-Month')['Vehicle Number'].count()

# Visualize the results
plt.figure(figsize=(12, 8))
monthly_yearly_shipments.plot(kind='bar')
plt.title('Number of Vehicles Shipped Each Month and Year')
plt.xlabel('Month and Year')
plt.ylabel('Number of Vehicles')
plt.xticks(rotation=45)
plt.show()