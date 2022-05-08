api_key = 'a64fadec7ec7420cb83b631a2f1b203a'    
from joblib import PrintTime
import requests
import pandas as pd
import streamlit as st
import numpy as np
import os
import urllib.request
import json
import configparser
import codecs
import requests
from bs4 import BeautifulSoup
import re

st.title('News summarize')
form = st.form(key='my_form')
input = form.text_area(label='write here',max_chars=140,placeholder='ここに入力')
submit_button = form.form_submit_button(label='Submit')


headers = {'X-Api-Key': 'a64fadec7ec7420cb83b631a2f1b203a'}
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'category' : 'business',
    'country' : 'jp',
    'pageSize' : 10
}
response = requests.get(url, headers=headers, params=params)
#pd.options.display.max_colwidth = 25
if response.ok:
    data = response.json()
    df = pd.DataFrame(data['articles'])
    #print('totalResults:', data['totalResults'])

#print(df[['publishedAt','title','url']])
a = df['url'][1]
print(a)
vgm_url = a
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser',from_encoding='utf-8')
print(soup.title.string)
