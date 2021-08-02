# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

options = webdriver.ChromeOptions()
# 以下のオプションを有効にするとヘッドレスモード
options.add_argument('--headless')

# 事前作業としてChromeDriverにパスを通しておく
driver = webdriver.Chrome(options=options)

# Qiitaトレンドのタイトルを取得して出力する

driver.get('https://qiita.com')
for title in driver.find_elements_by_css_selector("article h2"):
    print(title.text)

# Qiitaトップページから"python"を検索して一覧表示後、トップ記事を開く
search = driver.find_element_by_class_name("st-RenewalHeader_searchInput")
search.send_keys("python")
search.submit()

print("================== search 'python' =========================")

for title in driver.find_elements_by_class_name("searchResult_itemTitle"):
    print(title.text)

driver.quit()
