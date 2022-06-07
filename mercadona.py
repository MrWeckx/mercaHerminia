#%%
from numpy import product
from regex import F
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from random import randint,shuffle
from tqdm import tqdm
import datetime

import sys 
sys.path.insert(0,"~/Driver/chromedriver_linux64")

#%% Tdos que se me ocurren
# TODO test productos que quiero que estén en la subida
# TODO precio por kilo
# TODO correlación precio kilo

# Mercadona Categories
categories_pages = [112, 115, 116, 117,
                    156,163,158,159,161,162,
                    135,133,132,
                    118,121,120,
                    89,95,92,97,90,
                    216,217,218,219,
                    164,166,181,174,168,170,169,173,
                    86,81,83,84,88,
                    46,38,47,37,40,42,43,44,45,
                    78,79,80,
                    48,52,49,50,51,53,54,56,58]

#%%

def find_all_available_categories(driver):
    """
    Find all available categories in mercadona based on range

    Parameters

    driver: selenium webdriver
    return: tuple(list of available categories, list of empty categories)
    """
    min_cat=40
    max_cat=200
    category_found=[]
    empty_cat=[]
    categories_to_search=[*range(min_cat,max_cat)]
    shuffle(categories_to_search)
    for i in tqdm(categories_to_search):
        driver.get('https://tienda.mercadona.es/categories/'+str(i))
        time.sleep(randint(4,6))
        if 'categories' in driver.current_url:
            category_found.append(i)
        else:
            empty_cat.append(i)
    return category_found,empty_cat

#%%
def get_mercadona_product_cells(soup):
    merc_cell=[]
    for tag in soup.findAll('div', attrs={'class':'product-cell__info'}):
        merc_cell.append(tag)
    return merc_cell

#%%
def get_table_register_from_product_cell(cell):
    # print(item)
    # print('Name')
    name="".join([t.text for t in cell.findAll('h4', attrs={'class':'subhead1-r product-cell__description-name'})])
    print(name)
    # print('Unit')
    unit="".join([t.text for t in cell.findAll('span')])
    print(unit)
    # print('Price')
    price=cell.findAll('div', attrs={'class':'product-price'})[0].text
    print(price)
    return((name,unit,price))


#%%
def initialize_mercadona_web_driver():
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()

    driver.get('https://tienda.mercadona.es/categories/112')
    time.sleep(10)
    element=driver.find_element_by_name("postalCode")
    element.send_keys('28043')
    # element.find_element_by_tag_name("BUTTON").click()
    element.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/div/form/button/span").click()
    time.sleep(5)
    return driver

#%%
def search_and_save_categories(driver):
    categories_pages_true=find_all_available_categories(driver)
# %%
    with open('current_categories.txt','w') as f:
        f.write(str(", ".join([str(e) for e in categories_pages_true[0]])))
# %%
    with open('bad_categories.txt','w') as f:
        f.write(str(", ".join([str(e) for e in categories_pages_true[1]])))
    
#%%
def load_current_categories():
    with open('current_categories.txt','r') as f:
        current_categories=f.read()
    current_categories=current_categories.split(', ')
    return current_categories

#%%
def travel_through_categories_and_generat_dict_categories(driver,categories_pages):
    dict_pages={}
    for page_id in tqdm(categories_pages):
        page='https://tienda.mercadona.es/categories/'+str(page_id)
        driver.get(page)
        time.sleep(8)
        soup= BeautifulSoup(driver.page_source, 'html.parser')
        product_data=[get_table_register_from_product_cell(cell) for cell in get_mercadona_product_cells(soup)]
        dict_pages[page_id]=product_data
        print(f'For {page_id} we have {len(product_data)} products')
    return dict_pages

#%%

def append_current_dict_pages_to_mercadona_df(dict_pages):
    df_base=pd.DataFrame(data=[('a','a','a','a')],columns=['name','unit','price','category'])
    for category,data_category in dict_pages.items():
        print('For category: '+str(category)+ ' there are '+str(len(data_category))+' products')
        df=pd.DataFrame(data_category,columns=['name','unit','price'])
        df['category']=str(category)
        df_base=pd.concat([df_base.copy(),df.copy()])

    df_grouped_cat=df_base.groupby(['name','unit','price'],as_index=False).agg({'category':lambda x:', '.join(x)})


    df_grouped_cat['date']=datetime.datetime.today().strftime("%Y-%m-%d")
    df_grouped_cat=df_grouped_cat[['date','name','unit','price','category']]

    # Mercadona df
    df_mercadona=pd.read_csv('mercadona_products_tot.csv',sep=';')

    df_new=pd.concat([df_mercadona.copy(),df_grouped_cat.copy()])

    df_new.to_csv('mercadona_products_tot.csv',sep=';',index=False)