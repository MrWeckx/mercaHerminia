#%%
import pandas as pd

productos=pd.read_csv('mercadona_products_tot.csv',sep=';')
productos=productos[productos.name.ne('a')]

#%%
productos['price_euros']=productos['price'].str.replace(',','.').apply(lambda x: float(x.split('€')[0]))
productos['unit']=productos['price'].str.replace(',','.').apply(lambda x: x.split('€')[1]).str.replace('/','')
productos

#%%
avg_price=productos.price_euros.mean()
avg_price
#%% Avg price per category
productos.groupby('category').price_euros.mean()

#%% Total number of products
productos.name.drop_duplicates().count()

#%% 
registros_cafes=productos.name.str.contains('café')

productos[registros_cafes]

#%%
tamaño_file=322000
en_30_dias_mb=tamaño_file*30/1024/1024

