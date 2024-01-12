from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import sqlite3

# ブラウザをheadlessモード実行
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wait = WebDriverWait(options,10)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

url = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=12&day=&view="
driver.get(url)
time.sleep(3)

# データベースへの挿入
path = '/Users/naoki/Lecture/ds_program_health/'
db_name = 'weather12.sqlite'
con = sqlite3.connect(path + db_name)
cur = con.cursor()

# テーブルの作成
cur.execute('''
    CREATE TABLE weather12 (
        day INTEGER,
        hpa REAL,
        temp_ave REAL,
        temp_max REAL,
        temp_min REAL,
        humidity_ave INTEGER,
        humidity_min INTEGER,
        sun REAL
    );
''')

for date in range(5, 36):  # Adjusted range to match the number of rows on the page
    data = {}
    
    data['day'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[1]/div/a').text
    data['hpa'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[2]').text  # Adjusted column index
    data['temp_ave'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[7]').text
    data['temp_max'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[8]').text
    data['temp_min'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[9]').text
    data['humidity_ave'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[10]').text
    data['humidity_min'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[11]').text  # Adjusted column index
    data['sun'] = driver.find_element(By.XPATH, f'//*[@id="tablefix1"]/tbody/tr[{date}]/td[17]').text  # Adjusted column index
    
    # データの挿入
    sql_insert_data = '''
        INSERT INTO weather12 (day, hpa, temp_ave, temp_max, temp_min, humidity_ave, humidity_min, sun)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cur.execute(sql_insert_data, (data['day'], data['hpa'], data['temp_ave'], data['temp_max'], data['temp_min'], data['humidity_ave'], data['humidity_min'], data['sun']))

# データベースの変更を保存
con.commit()

# データベース接続をクローズ
con.close()

# ブラウザを終了
driver.quit()