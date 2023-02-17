import os
import time
import datetime
import pandas as pd

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# グリーン
def green():
    
    occupation = input("職種を入力してください：")
    count = input("取得数を入力してください：")
    
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
    url = "https://www.green-japan.com/"
    
    driver.get(url)
    time.sleep(1)
    
    driver.find_element(by=By.CSS_SELECTOR, value=".js-search-keyword").send_keys(occupation)
    driver.find_element(by=By.CSS_SELECTOR, value=".js-header-search-submit").click()
    time.sleep(3)
    
    jobs = driver.find_elements(by=By.CSS_SELECTOR, value=".card-info__wrapper")
    
    offer_cnt = 0
    for job in jobs:
        # 求人名
        try:
            name = job.find_element(by=By.CSS_SELECTOR, value=".card-info__heading-area__title").text
        except:
            name = ""
        # 会社名
        try:
            company = job.find_element(by=By.CSS_SELECTOR, value=".card-info__detail-area__box__title").text
        except:
            company = ""
        # メタタグ
        try:
            meta_tags = job.find_element(by=By.CSS_SELECTOR, value=".job-offer-meta-tags")
        except:
            meta_tags = ""
        # 給与
        try:
            salary = meta_tags.find_elements(by=By.CSS_SELECTOR, value="li")[0].text
        except:
            salary = ""
        # 勤務地
        try:
            pref = meta_tags.find_elements(by=By.CSS_SELECTOR, value="li")[1].text
        except:
            pref = ""
        # 詳細URL
        try:
            detail_url = job.find_element(by=By.CSS_SELECTOR, value=".js-search-result-box").get_attribute("href")
        except:
            detail_url = ""
            
        item_info.append({
            "企業名": company,
            "求人名": name,
            "給与": salary,
            "勤務地": pref,
            "詳細ページ": detail_url,
        })
        
        offer_cnt += 1
        if offer_cnt == count:
            break
    
    return item_info

# CSVファイルパス
EXP_CSV_PATH = "green_csv/exp_list_{datetime}.csv"

# ファイルの作成
def makedir_for_filepath(filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

# メイン処理
def main():
    
    item_info = green()
        
    # CSVファイル保存処理
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    makedir_for_filepath(EXP_CSV_PATH) 
    df = pd.DataFrame.from_dict(item_info, dtype=object)
    df.to_csv(EXP_CSV_PATH.format(datetime=now), encoding="utf-8-sig")
        
if __name__ == "__main__":        
    main()
