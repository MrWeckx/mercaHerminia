#%%
import pandas as pd
import numpy as np

productos=pd.read_csv('mercadona_products_tot.csv',sep=';')
productos=productos[productos.name.ne('a')]

#%% 
print('Fecha máxima',productos.date.max())
# print('N fechas unique',productos.date.unique())
# print('Regs partido len unique',productos.shape[0]/len(productos.date.unique()))
print('N prods por fecha',productos.date.value_counts())

#%% Columnas adicionales
productos['price_euros']=productos['price'].str.replace(',','.').apply(lambda x: float(x.split('€')[0]))
productos['unit']=productos['price'].str.replace(',','.').apply(lambda x: x.split('€')[1]).str.replace('/','')
productos['name_unit']=productos['name'] + ' ' +productos['unit']
productos

#%%
avg_price=productos.price_euros.mean()
avg_price
#%% Avg price per category
productos.groupby('category').price_euros.mean()

#%% Total number of products
productos.name.drop_duplicates().count()


#%% Producto que ha tenido más diferencia relativa de precio en 3 días
productos[['date','name_unit','price_euros']]
precios_historicos=productos[['date','name_unit','price_euros']].pivot_table(index='date',columns='name_unit',values='price_euros',aggfunc='max')
precios_historicos

#%% Fluctuaciones del precio
# precios_historicos['Zumo de tomate Hacendado  pack'].plot()
precios_historicos['Galletas Digestive avena Hacendado  ud.'].plot()
#%%
precios_historicos['diff_precio_porcentual']=np.abs(precios_historicos['2022-06-01']-precios_historicos['2022-06-03'])/precios_historicos['2022-06-01']
precios_historicos[precios_historicos.diff_precio_porcentual==precios_historicos.diff_precio_porcentual.max()]

#%%
precios_historicos[precios_historicos.diff_precio_porcentual>0.05]

#%% Fluctuación del precio de un producto en el tiempo


#%%

# productos.pivot(index='name',columns='date',values='price_euros').diff(axis=1).max(axis=1)
precio_hist=productos[['date','name_unit','price_euros']].drop_duplicates().pivot(index='date',columns='name_unit')['price_euros']
precio_hist

#%% 
registros_cafes=productos.name.str.contains('café')

productos[registros_cafes]

#%%
tamaño_file=322000
en_30_dias_mb=tamaño_file*30/1024/1024
en_30_dias_mb*12
