# Locate the starting point of "Tops" and "Bottoms" for Plant 1
tops_index = data[data.iloc[:, 0] == 'Tops'].index[0]
bottoms_index = data[data.iloc[:, 0] == 'Bottoms'].index[0]

# Assuming the data structure repeats, find the end of the Tops section for Plant 1
end_tops_index = bottoms_index - 1  # The row before Bottoms starts

# Extract the "Tops" section for Plant 1
tops_data = data.iloc[tops_index+1:end_tops_index]

# Clean and structure the data
# We need to determine how many rows belong to the header to parse the station tables correctly
# Let's first display the extracted "Tops" section to adjust the header parsing if necessary
tops_data.head(20)
