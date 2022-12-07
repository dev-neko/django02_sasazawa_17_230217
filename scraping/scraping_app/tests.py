from django.test import TestCase

# Create your tests here.


import os
import time
import datetime
import pandas as pd

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint
from selenium.webdriver.common.keys import Keys

# メイン処理
def geekly(occupation, count):
    
    # ドライバの定義
    def set_driver():
        '''
        Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
        '''
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        options = ChromeOptions()

        # 起動オプションの設定
        options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
        options.add_argument('log-level=3') # 不要なログを非表示にする
        options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
        options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
        # options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
        options.add_argument('--incognito') # シークレットモードの設定を付与
        
        # ChromeのWebDriverオブジェクトを作成する。
        service=Service(ChromeDriverManager().install())
        return Chrome(service=service, options=options)

    item_info = []
    driver = set_driver()
    url = "https://www.geekly.co.jp/"
    
    driver.get(url)
    time.sleep(1)
    driver.find_element(by=By.CSS_SELECTOR, value="#header_search").click()
    time.sleep(2)
    driver.find_element(by=By.CSS_SELECTOR, value="#search_keyword").send_keys(occupation)
    driver.find_element(by=By.CSS_SELECTOR, value=".header_search_submit").click()
    time.sleep(5)
    
    jobs = driver.find_elements(by=By.CSS_SELECTOR, value=".recruitment_item")
    
    offer_cnt = 0
    for job in jobs:
        # 求人タイトル
        try:
            head = job.find_element(by=By.CSS_SELECTOR, value=".recruitment_head")
        except:
            head = ""
            continue
        # 求人名
        try:
            name = head.find_element(by=By.TAG_NAME, value="h2").find_element(by=By.TAG_NAME, value="a").text
        except:
            name = ""
         # 会社名
        try:
            company = head.find_element(by=By.CSS_SELECTOR, value=".company_name").find_element(by=By.TAG_NAME, value="a").text
        except:
            company = ""
            
        print(name)
        print(company)
        # 給与
        try:
            salary = job.find_elements(by=By.CSS_SELECTOR, value=".recruitment_content_row")[0].find_element(by=By.TAG_NAME, value="dd").text
        except:
            salary = ""
        # 勤務地
        try:
            pref = job.find_elements(by=By.CSS_SELECTOR, value=".recruitment_content_row")[1].find_element(by=By.TAG_NAME, value="dd").text
        except:
            pref = ""
            
        print(salary)
        print(pref)
    #     # 詳細URL
        try:
            detail_url = job.find_element(by=By.CSS_SELECTOR, value=".to_detail").find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        except:
            detail_url = ""
        print(detail_url)
            
    #     item_info.append({
    #         "企業名": company,
    #         "求人名": name,
    #         "給与": salary,
    #         "勤務地": pref,
    #         "詳細ページ": detail_url,
    #     })
        
    #     offer_cnt += 1
    #     if offer_cnt == count:
    #         break
    

    # scope = ['https://spreadsheets.google.com/feeds',
    #         'https://www.googleapis.com/auth/drive']
    # json_keyfile_path = 'django02-sasazawa-17-99306970c260.json'

    # # サービスアカウントキーを読み込む
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(
    #     json_keyfile_path, scope)

    # # pydrive用にOAuth認証を行う
    # gauth = GoogleAuth()
    # gauth.credentials = credentials
    # drive = GoogleDrive(gauth)

    # folder_id = '1_zD09wn0ufd2znqBMZcy2qOQBsmrKdIU'
    # now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # EXP_FILE = f"exp_list_{now}"
    # f = drive.CreateFile({
    #     'title': EXP_FILE,
    #     'mimeType': 'application/vnd.google-apps.spreadsheet',
    #     "parents": [{"id": folder_id}]})
    # f.Upload()

    # # 作成したスプレッドシートの情報を出力
    # pprint.pprint(f)

    # # gspread用に認証
    # gc = gspread.authorize(credentials)

    # # スプレッドシートのIDを指定してワークブックを選択
    # workbook = gc.open_by_key(f['id'])
    # worksheet = workbook.sheet1
    
    # # 1行目の1~3列目に入力
    # worksheet.update_cell(1, 1, '企業名')
    # worksheet.update_cell(1, 2, '求人名')
    # worksheet.update_cell(1, 3, '給与')
    # worksheet.update_cell(1, 4, '勤務地')
    # worksheet.update_cell(1, 5, '詳細ページ')
    
    # cnt = 2
    # for item in item_info:
    #     worksheet.update_cell(cnt, 1, item['企業名'])
    #     worksheet.update_cell(cnt, 2, item['求人名'])
    #     worksheet.update_cell(cnt, 3, item['給与'])
    #     worksheet.update_cell(cnt, 4, item['勤務地'])
    #     worksheet.update_cell(cnt, 5, item['詳細ページ'])
    #     cnt += 1
        
    #     print(item_info)
    
geekly(occupation = "データサイエンティスト", count=1)
