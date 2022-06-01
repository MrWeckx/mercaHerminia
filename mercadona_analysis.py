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