#%%
from calendar import LocaleTextCalendar
from numpy import product
from regex import F
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from random import randint,shuffle
from tqdm import tqdm
import datetime
from random import randint,shuffle

import sys 
import os

from secrets import NEXTCLOUD_DATA_ROUTE_SECRET
sys.path.insert(0,"~/Driver/chromedriver_linux64")

from mercadona import *
from secrets import *

NEXTCLOUD_DATA_ROUTE=NEXTCLOUD_DATA_ROUTE_SECRET

if __name__ == '__main__':
    # driver=initialize_mercadona_web_driver()
    # current_categories=load_current_categories()
    # dict_res=travel_through_categories_and_generat_dict_categories(driver,current_categories)
    # append_current_dict_pages_to_mercadona_df(dict_res)
    
    # Lo llevamos al nextcloud
    os.system(f'cp mercadona_products_tot.csv {NEXTCLOUD_DATA_ROUTE}/mercadona_products_tot.csv')
# %%
