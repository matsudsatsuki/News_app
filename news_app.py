#api_key = 'a64fadec7ec7420cb83b631a2f1b203a'    
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
from newspaper import Article
import nltk
import time
nltk.download('punkt')

st.title('News summarize')
option = False
option = st.selectbox(
        'Choose the category',
        ('business','entertainment','general','health','science','sports','technology'),
        )
#headers = {'X-Api-Key': 'a64fadec7ec7420cb83b631a2f1b203a'}
#url = 'https://newsapi.org/v2/top-headlines'

if option:
    headers = {'X-Api-Key': 'a64fadec7ec7420cb83b631a2f1b203a'}
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'category' : option,
        'country' : 'jp',
        'pageSize' : 10
    }
    response = requests.get(url, headers=headers, params=params)
    pd.options.display.max_colwidth = 25
    if response.ok:
        data = response.json()
        df = pd.DataFrame(data['articles'])
        #print('totalResults:', data['totalResults'])

    #print(df[['publishedAt','title','url']])

    st.write('You selected:', option)
    URL = df['url'][0]
    #url1 = 'https://news.yahoo.co.jp/pickup/6426184'
    article = False
    article = Article(URL)
    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()
    ans = article.summary

    st.write(article.text)
    form = st.form(key='my_form')
    input = form.text_area(label='write here',max_chars=140,placeholder='ここに入力')
    submit_button = form.form_submit_button(label='Submit')
    my_bar = st.progress(0)
    for percent_complete in range(61):
        time.sleep(1)
        my_bar.progress(percent_complete + 1)


# COTOHA API操作用クラス
class CotohaApi:
    # 初期化
    def __init__(self, client_id, client_secret, developer_api_base_url, access_token_publish_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_api_base_url = developer_api_base_url
        self.access_token_publish_url = access_token_publish_url
        self.getAccessToken()
    # アクセストークン取得
    def getAccessToken(self):
        # アクセストークン取得URL指定
        url = self.access_token_publish_url

        # ヘッダ指定
        headers={
            "Content-Type": "application/json;charset=UTF-8"
        }

        # リクエストボディ指定
        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()

        # リクエスト生成
        req = urllib.request.Request(url, data, headers)

        # リクエストを送信し、レスポンスを受信
        res = urllib.request.urlopen(req)

        # レスポンスボディ取得
        res_body = res.read()

        # レスポンスボディをJSONからデコード
        res_body = json.loads(res_body)

        # レスポンスボディからアクセストークンを取得
        self.access_token = res_body["access_token"]
    # 類似度算出API
    def similarity(self, s1, s2):
        # 類似度算出API URL指定
        url = self.developer_api_base_url + "v1/similarity"
        # ヘッダ指定
        headers={
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json;charset=UTF-8",
        }
        # リクエストボディ指定
        data = {
            "s1": s1,
            "s2": s2
        }
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()
        # リクエスト生成
        req = urllib.request.Request(url, data, headers)
        # リクエストを送信し、レスポンスを受信
        try:
            res = urllib.request.urlopen(req)
        # リクエストでエラーが発生した場合の処理
        except urllib.request.HTTPError as e:
            # ステータスコードが401 Unauthorizedならアクセストークンを取得し直して再リクエスト
            if e.code == 401:
                print ("get access token")
                self.access_token = getAccessToken(self.client_id, self.client_secret)
                headers["Authorization"] = "Bearer " + self.access_token
                req = urllib.request.Request(url, data, headers)
                res = urllib.request.urlopen(req)
            # 401以外のエラーなら原因を表示
            else:
                print ("<Error> " + e.reason)

        # レスポンスボディ取得
        res_body = res.read()
        # レスポンスボディをJSONからデコード
        res_body = json.loads(res_body)
        # レスポンスボディから解析結果を取得
        return res_body








if __name__ == '__main__' and input:
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"

    # 設定値取得
    config = configparser.ConfigParser()
    config.read(APP_ROOT + "config.ini")
    CLIENT_ID = config.get("COTOHA API", "Developer Client id")
    CLIENT_SECRET = config.get("COTOHA API", "Developer Client secret")
    DEVELOPER_API_BASE_URL = config.get("COTOHA API", "Developer API Base URL")
    ACCESS_TOKEN_PUBLISH_URL = config.get("COTOHA API", "Access Token Publish URL")

    # COTOHA APIインスタンス生成
    cotoha_api = CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 解析対象文
    

    #構文解析API実行
    result = cotoha_api.similarity(input,ans)
    score = result['result']
    final_score = score['score']
    if int(final_score*10) > 6:
        st.write('Correct answer')
        st.balloons()
    else:
        st.write('You are wrong')
        #st.snow()
    st.write(final_score)
    st.write(ans)
    #print(result)
    # 出力結果を見やすく整形
    #result_formated = json.dumps(result, indent=4, separators=(',', ': '))
    #print(codecs.decode(result_formated, 'unicode-escape'))
