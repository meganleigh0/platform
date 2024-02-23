import pandas as pd
from collections import defaultdict

def search_swh(df):
    swh = pd.read_csv('assets/standards.csv')
  
    # Extract unique part numbers and filter labor standards
    pnums = df['PartNumber'].unique()
    ref_standards = swh[swh['PlanNo'].isin(pnums)].drop_duplicates(subset=['PlanNo', 'Operation Desc'])
    
    # Merge df with ref_standards on PartNumber == PlanNo
    merged_df = pd.merge(df, ref_standards, left_on='PartNumber', right_on='PlanNo')
    
    # Create a defaultdict to store operation data
    op_data = defaultdict(list)
    for _, row in merged_df.iterrows():
        hrs = row['SFC']
        desc = row['Operation Desc']
        dept = int(row['Department'])
        
        # Append [hrs, desc, dept] information to the operation dictionary, keyed to mbomID
        op_data[row['mbomID']].append([hrs, desc, dept])
    
    return dict(op_data)
