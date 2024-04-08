# Load department data used for simulation input
dep_df = pd.read_csv(os.path.join(project_root, "assets", "data", "department_data.csv"))
dep_df['DepID'] = dep_df['DepID'].astype(str)

# Merge dataframes using a left join to keep all entries in dep_df
merged_df = pd.merge(dep_df, exp_df[['Department', 'DirectEmployee']], left_on='DepID', right_on='Department', how='left')

# Update 'DirectHeads' only where new data is available, preserve existing otherwise
dep_df['DirectHeads'] = merged_df['DirectEmployee'].combine_first(dep_df['DirectHeads']).astype(int)

# Now dep_df contains the updated department data
try:
    dep_df.to_csv(os.path.join("assets", "data", "department_data_updated.csv"), index=False)
except Exception as e:
    print(f"Error exporting department data: {e}")