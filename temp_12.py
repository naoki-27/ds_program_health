from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import re
import sqlite3

# ブラウザをheadlessモード実行
options = webdriver.ChromeOptions()
#ヘッドレスモード（バックグラウンドで起動）で実行。コラボの場合、必須。
options.add_argument('--headless')
#サンドボックスモードの解除。これも必須。
options.add_argument('--no-sandbox')
#これも設定した方がよい。
options.add_argument('--disable-dev-shm-usage')
wait = WebDriverWait(options,10)

driver = webdriver.Chrome()
#指定したドライバーが見つかるまで待機
driver.implicitly_wait(10)

#urlの指定
url="https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=12&day=&view="

driver.get(url)
time.sleep(3)

weather_data_2023_12 = []

for date in range(5, 36):
    data = {}
    
    data['day'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[1]/div/a').text
    data['hpa'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[2]').text
    data['temp_ave'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[7]').text
    data['temp_max'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[8]').text
    data['temp_min'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[9]').text
    data['humidity_ave'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[10]').text
    data['humidity_min'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[11]').text
    data['sun'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[17]').text
    
    weather_data_2023_12.append(data)

# データベースへの挿入
path = '/Users/naoki/Lecture/ds_program_health/'
db_name = 'sleep.sqlite'
con = sqlite3.connect(path + db_name)
cur = con.cursor()

# データの挿入
for data in weather_data_2023_12:
    sql_insert_data = '''
        INSERT INTO weather12 (day, hpa, temp_ave, temp_max, temp_min, humidity_ave, humidity_min, sun)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cur.execute(sql_insert_data, (data['day'], data['hpa'], data['temp_ave'], data['temp_max'], data['temp_min'], data['humidity_ave'], data['humidity_min'], data['sun']))

# データベースの変更を保存
con.commit()