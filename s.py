import pandas as pd

# Parse sheet from workbook
df = sep_operations.parse(sep_operations.sheet_names[0], skiprows=0).fillna(0)

# Function to clean and convert column to float
def clean_and_convert(column):
    # Convert to string
    column = column.astype(str)
    # Replace unwanted characters
    column = column.str.replace(' ', '').str.replace(',', '.').str.replace('(', '').str.replace(')', '').str.replace('-.-', '0')
    # Remove any remaining non-numeric characters except for the decimal point
    column = column.str.replace('[^0-9.]', '', regex=True)
    print("Column after cleaning:")
    print(column.head(10))
    return column.astype(float)

# Apply the function to the columns
try:
    df["Common"] = clean_and_convert(df["Common"])
    print("After conversion to float (Common):")
    print(df["Common"].head(10))
except ValueError as e:
    print(f"Error converting 'Common': {e}")
    print(df["Common"].unique())

try:
    df["SEPV3"] = clean_and_convert(df["SEPV3"])
    print("After conversion to float (SEPV3):")
    print(df["SEPV3"].head(10))
except ValueError as e:
    print(f"Error converting 'SEPV3': {e}")
    print(df["SEPV3"].unique())

# Check if both columns have been converted correctly
if df["Common"].dtype == 'float64' and df["SEPV3"].dtype == 'float64':
    df["Hours"] = (df["Common"] + df["SEPV3"])/60
    df = df[["Hours"]].copy()
    print(f"{sep_operations.sheet_names[0]}, Length: {len(df)}")
    print(df.head(10))
else:
    print("Conversion to float failed for one or both columns.")