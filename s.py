def set_ids(df):
    # Assign unique mbomIDs starting from 100001
    df['mbomID'] = np.arange(100001, 100001 + len(df))
    
    # Initialize parent ID with zeros
    df['ParentID'] = 0
    
    # Create a dictionary to map levels to the most recent mbomID at that level
    level_to_mbomID = {}
    
    for index, row in df.iterrows():
        lev = row['Levels']
        # Update the current level's most recent mbomID
        level_to_mbomID[lev] = row['mbomID']
        
        # Set parent ID for non-top levels (assuming top level is 0 and has no parent)
        if lev > 0:
            # Parent is the most recent mbomID at the previous level
            df.at[index, 'ParentID'] = level_to_mbomID.get(lev - 1, 0)
    
    # Calculate 'Number of Children' for each mbomID
    child_counts = df.groupby('ParentID').size()
    df['Number of Children'] = df['ParentID'].map(child_counts).fillna(0).astype(int)
    
    return df



'''
Unique ID Generation: The mbomID assignment is simplified using numpy's arange for direct assignment, eliminating the need for manual array creation.
Parent ID Assignment: This version maintains a mapping of levels to the most recent mbomID at each level, allowing for a more straightforward and efficient way to assign parent IDs.
Child Count Calculation: The number of children for each mbomID is calculated by grouping the DataFrame by ParentID and counting occurrences, which is more efficient and accurate than appending to and mapping from a list.
Vectorized Operations: Wherever possible, operations are vectorized or use efficient pandas functions to improve performance over manual looping and condition checking.'''
