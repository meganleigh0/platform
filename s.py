def organize_by_user_org(self):
    # Example of separating the DataFrame into different attributes
    self.df_lim = self.df[self.df["Usr Org"] == "LIM"]
    self.df_scr = self.df[self.df["Usr Org"] == "SCR"]
    self.df_tlh = self.df[self.df["Usr Org"] == "TLH"]

    # Optionally, log the size of each split to keep track
    print(f"LIM records: {len(self.df_lim)}")
    print(f"SCR records: {len(self.df_scr)}")
    print(f"TLH records: {len(self.df_tlh)}")

    # If there are further steps that are specific to each organization,
    # you can call those methods here. For example:
    # self.process_lim()
    # self.process_scr()
    # self.process_tlh()
def process_mbom(var):
    # Initial data loading and preprocessing
    df = load_mbom(var)  # Assuming load_mbom returns the correct DataFrame
    
    initial_size = len(df)
    print(f"Initial number of records: {initial_size}")

    # Example of filtering rows (e.g., removing unwanted rows)
    before_filtering = len(df)
    df = df[(df['Supply'] != 'Bulk') & (df['Supply'] != 'Phantom')]  # Adjust condition as needed
    after_filtering = len(df)
    print(f"Records removed by filtering 'Supply': {before_filtering - after_filtering}")

    # Dropping NaN values in 'Qty' column
    before_dropna = len(df)
    df.dropna(subset=['Qty'], inplace=True)
    after_dropna = len(df)
    print(f"Records dropped after dropping NaN in 'Qty': {before_dropna - after_dropna}")
