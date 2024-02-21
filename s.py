import pandas as pd
import numpy as np
import re

def load_mbom(variant): 
    # Load CSV file into DataFrame
    mbom = pd.read_csv(f"assets/{variant}.csv")
    print("Initial DataFrame loaded:", mbom.shape)

    # Copy mbom data frame
    df = mbom.copy()
    
    # Remove leading and trailing spaces and replace with empty string
    df = df.replace(r"^ +| +$", r"", regex=True)
    print("After trimming spaces:", df.shape)
    
    # Remove hyphen from 'Part Number' column
    df.rename(columns={'Part-Number': 'PartNumber'}, inplace=True)
    print("After renaming 'Part-Number' to 'PartNumber':", df.shape)
   
    # Remove rows with 'Supply' column value equal to "Bulk" (ROP/trivial parts) and "Phantom"
    df = df.loc[(df['Supply'] != 'Bulk') & (df['Supply'] != 'Phantom')]
    print("After removing rows with 'Supply' = 'Bulk' or 'Phantom':", df.shape)

    # Clean descriptions (apply clean_description function)
    df['Description'] = df['Description'].astype(str)
    df['Description'] = df['Description'].apply(clean_description)
    print("After cleaning descriptions:", df.shape)
    
    # Cast Quantity as integer
    df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
    df['Qty'] = df['Qty'].apply(to_int_or_nan)
    df.dropna(subset=['Qty'], inplace=True)
    df['Qty'] = df['Qty'].astype(int)
    print("After casting 'Qty' to integer and dropping NaN:", df.shape)
   
    # Extract plant DataFrames by "Usr Org"
    df_lim = df[df["Usr Org"] == "LIM"]
    df_scr = df[df["Usr Org"] == "SCR"]
    df_tlh = df[df["Usr Org"] == "TLH"]
    print("After extracting plant-specific DataFrames:", f"LIM: {df_lim.shape}, SCR: {df_scr.shape}, TLH: {df_tlh.shape}")

    # Drop columns not required for use in model functions
    columns_to_drop = [
        'Item No', 'Ext Qty', 'Type', 'Sre Org', 'Dis Date', 'Supply',
        'Fixed Order Qty', 'Planning Method', 'Long Description'
    ]
    df_lim.drop(columns=columns_to_drop, inplace=True)
    df_scr.drop(columns=columns_to_drop, inplace=True)
    df_tlh.drop(columns=columns_to_drop, inplace=True)
    print("After dropping unnecessary columns:", f"LIM: {df_lim.shape}, SCR: {df_scr.shape}, TLH: {df_tlh.shape}")
    
    # Return a list of DataFrames sorted by plant
    data = [mbom, df_lim, df_scr, df_tlh]
    return data

def clean_description(desc):
    # Assume this function is defined elsewhere with the correct logic
    pass

def to_int_or_nan(val):
    # Assume this function is defined elsewhere with the correct logic
    pass
