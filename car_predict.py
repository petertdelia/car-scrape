import pandas as pd

df = pd.read_csv('df_cars.csv', index_col=0)

# drop indexes with missing number values
df = df.dropna()

df['mileage'] = df['mileage'].replace({'Miles':''})
df['mileage'] = pd.to_numeric(df['mileage'])

# again, drop indexes with missing number values (this is because of a flaw in the mileage column which breaks the .to_numeric() function if I don't call dropna first)
# need to correct the way the list gets created, so that if the trim is missing (or any entry is missing) the program will still insert an empty data point 
df = df.dropna()

# drop irrelevant columns (when years, makes, and models are all equivalent)
df = df.drop(columns={'year','make','model'})

df = df.reset_index(drop=True)
