api_key = 'a64fadec7ec7420cb83b631a2f1b203a'    
from joblib import PrintTime
import requests
import pandas as pd

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
    print('totalResults:', data['totalResults'])

#print(df[['publishedAt','title','url']])
a = df['url'][0]
print(a)