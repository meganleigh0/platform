import pandas as pd

# Parse sheet from workbook
df = sep_operations.parse(sep_operations.sheet_names[0], skiprows=0).fillna(0)

# Function to clean and convert column to numeric
def clean_and_convert(column):
    # Convert to string and replace unwanted characters
    column = column.astype(str)
    column = column.str.replace(' ', '').str.replace(',', '.').str.replace('(', '').str.replace(')', '').str.replace('-.-', '0')
    # Remove any remaining non-numeric characters except for the decimal point
    column = column.str.replace('[^0-9.]', '', regex=True)
    # Convert to numeric, coercing errors to NaN, then fill NaN with 0
    column = pd.to_numeric(column, errors='coerce').fillna(0)
    return column.astype(float)

# Apply the function to the columns
df["Common"] = clean_and_convert(df["Common"])
print("After conversion to float (Common):")
print(df["Common"].head(10))

df["SEPV3"] = clean_and_convert(df["SEPV3"])
print("After conversion to float (SEPV3):")
print(df["SEPV3"].head(10))

df["Hours"] = (df["Common"] + df["SEPV3"])/60
df = df[["Hours"]].copy()

print(f"{sep_operations.sheet_names[0]}, Length: {len(df)}")
print(df.head(10))