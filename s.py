from fuzzywuzzy import process
import pandas as pd

# Assuming your DataFrame is named df
# Assuming your list of assembly descriptions is named assembly_list

# Function to perform fuzzy matching and return the best match
def fuzzy_match(description, choices):
    return process.extractOne(description, choices)

# Assuming assembly_list is a list of assembly descriptions
matches = []
for assembly in assembly_list:
    match, score = fuzzy_match(assembly, df['Description'])
    matches.append((assembly, match, score))

# Convert the matches to a DataFrame for better visualization
matches_df = pd.DataFrame(matches, columns=['Assembly', 'Best Match', 'Score'])

# Display the matches
print(matches_df)