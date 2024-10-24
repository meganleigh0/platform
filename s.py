import pandas as pd

# Define the common parameters for each station
stations = [
    {'name': 'Turret Station 0', 'range': (124, 128)},
    {'name': 'Turret Station 1', 'range': (124, 128)},
    {'name': 'Turret Station 2/3/4', 'range': (124, 128)},
    # Add more stations here...
]

daily_dfs = []
for station in stations:
    st = test.parse(test.sheet_names[0], header=None).loc[station['range'][0]:station['range'][1], 0:6]
    st['Station'] = station['name']
    st['Date'] = test.sheet_names[0].split('Abrams ')[1].replace(' ', '').replace('.', '/')
    st.rename(columns={0: 'Contract', 2: 'MRP', 4: 'Actual', 5: 'Delta', 6: 'Flow'}, inplace=True)
    st.dropna(how='all', axis=1, inplace=True)
    st.drop(st.index[0], axis=0, inplace=True)
    daily_dfs.append(st)

# Concatenate all station dataframes into one
daily_df = pd.concat(daily_dfs)
daily_df