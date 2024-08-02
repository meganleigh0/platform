# Parse sheet from workbook
df = sep_operations.parse(sep_operations.sheet_names[0], skiprows=0).fillna(0)

# Convert columns to string and replace commas and spaces
df["Common"] = df["Common"].astype(str)
print("Before replacement (Common):")
print(df["Common"].head())
df["Common"] = df["Common"].str.replace(' ', '').str.replace(',', '.').str.replace('(', '').str.replace(')', '')
print("After replacement (Common):")
print(df["Common"].head())

# Convert to float
df["Common"] = df["Common"].astype(float)
print("After conversion to float (Common):")
print(df["Common"].head())

df["SEPV3"] = df["SEPV3"].astype(str)
print("Before replacement (SEPV3):")
print(df["SEPV3"].head())
df["SEPV3"] = df["SEPV3"].str.replace(' ', '').str.replace(',', '.').str.replace('(', '').str.replace(')', '')
print("After replacement (SEPV3):")
print(df["SEPV3"].head())

df["SEPV3"] = df["SEPV3"].astype(float)
print("After conversion to float (SEPV3):")
print(df["SEPV3"].head())

df["Hours"] = (df["Common"] + df["SEPV3"])/60
df = df[["Hours"]].copy()

print(f"{sep_operations.sheet_names[0]}, Length: {len(df)}")
print(df.head())