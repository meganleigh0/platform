    def preprocess(self):
        print("Preprocessing data...")
        # Filter rows
        self.df = self.df[(self.df['Supply'] != 'Bulk') & (self.df['Supply'] != 'Phantom')]
        
        # Clean descriptions
        self.df['Description'] = self.df['Description'].astype(str).apply(clean_description)
        
        # Handle 'Qty' column
        self.df['Qty'] = pd.to_numeric(self.df['Qty'], errors='coerce')
        before_dropna = len(self.df)
        self.df.dropna(subset=['Qty'], inplace=True)
        after_dropna = len(self.df)
        print(f"Records dropped after dropping NaN 'Qty': {before_dropna - after_dropna}")
        self.df['Qty'] = self.df['Qty'].astype(int)
        
        # Further preprocessing steps...
