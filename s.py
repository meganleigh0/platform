# Convert to DataFrame
df = pd.DataFrame(data)

# Convert tuple dates to datetime
df['Promise Date'] = df['Promise Date'].apply(lambda x: datetime(*x))
df['Ship Date'] = df['Ship Date'].apply(lambda x: datetime(*x))

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