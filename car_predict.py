import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# df = pd.read_csv('df_ford_used.csv',names=['year','make','model','trim','drive','mileage','price'], index_col=0)
df = pd.read_csv('explorer.csv',names=['year','make','model','trim','drive','mileage','price'],index_col=False)

df['price'] = pd.to_numeric(df['price'])
# drop indexes with missing number values
df = df.dropna()

# df['mileage'] = df['mileage'].replace({'Miles':''})
df['mileage'] = pd.to_numeric(df['mileage'])

# again, drop indexes with missing number values (this is because of a flaw in the mileage column which breaks the .to_numeric() function if I don't call dropna first)
# need to correct the way the list gets created, so that if the trim is missing (or any entry is missing) the program will still insert an empty data point 
df = df.dropna()

# drop irrelevant columns (when years, makes, and models are all equivalent)
df = df.drop(columns={'make','model'})

df = df.reset_index(drop=True)

df = df[(np.abs(stats.zscore(df['price'])) < 2.5)]

df_SE = df[df['trim'] == 'SE']
df_SEL = df[df['trim'] == 'SEL']
df_titanium = df[df['trim'] == 'Titanium']
df_sport = df[df['trim'] == 'Sport']
markers = ['ro','gs','b^','cv','mo','ys','k^','wv']
i=0
for trim in df.trim.unique():
    df_trim = df[df['trim'] == trim]
    plt.plot(df_trim['mileage'],df_trim['price'],markers[i])
    i+=1


# plt.plot(df_SEL['mileage'],df_SEL['price'],'ro',df_titanium['mileage'],df_titanium['price'],'gs',df_SE['mileage'],df_SE['price'],'b^',df_sport['mileage'],df_sport['price'],'cv')
plt.show()
