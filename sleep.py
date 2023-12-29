import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import sqlite3
import os

def scrape_and_insert():
    # ここにスクレイピングおよびデータベースへの挿入のコードを追加
    url = "https://tenki.jp/indexes/sleep/3/16/4410/13208/"
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    today_sleep = html_soup.find('section', class_="today-weather")

    date = today_sleep.find('h3', class_="left-style").text
    date_pattern = r"(\d+)月(\d+)日"
    date_match = re.search(date_pattern, date)

    if date_match:
        month = int(date_match.group(1))
        day = int(date_match.group(2))
        current_year = datetime.now().year
        date_result = datetime(current_year, month, day).date()
    else:
        date_result = None

    sleep_point = today_sleep.find('div', class_='indexes-icon-box').find('img').get('src')
    sleep_pattern = r'icon-large-(\d+)\.png'
    sleep_match = re.search(sleep_pattern, sleep_point)
    if sleep_match:
        sleep_point_result = float(sleep_match.group(1))
    else:
        sleep_point_result = None

    weather = today_sleep.find('div', class_="weather-icon-box")
    high_temp = float(weather.find('span', class_="high-temp").text.replace('℃', ''))
    low_temp = float(weather.find('span', class_="low-temp").text.replace('℃', ''))
    precip = float(weather.find('span', class_="precip").text.replace('%', ''))
    weather_climate = weather.find('p', class_="weather-telop").text
    coment = today_sleep.find('p', class_="indexes-telop-1").text

    sleep_dict = {
        "date": date_result,
        "sleep_point": sleep_point_result,
        "high_temperature": high_temp,
        "low_temperature": low_temp,
        "precip": precip,
        "weather": weather_climate,
        "coment": coment
    }

    # データベースへの挿入
    path = '/Users/naoki/Lecture/ds_program_health/'
    db_name = 'test1.sqlite'
    con = sqlite3.connect(path + db_name)
    cur = con.cursor()

    sql_insert_data = 'INSERT INTO test1 (date, sleep_point, high_temperature, low_temperature, precip, weather, coment) VALUES (?, ?, ?, ?, ?, ?, ?);'
    cur.execute(sql_insert_data, (
        sleep_dict["date"],
        sleep_dict["sleep_point"],
        sleep_dict["high_temperature"],
        sleep_dict["low_temperature"],
        sleep_dict["precip"],
        sleep_dict["weather"],
        sleep_dict["coment"]
    ))

    con.commit()
    con.close()


# # 定期的に実行
# if __name__ == "__main__":
#     # スクリプトのディレクトリを取得
#     script_directory = os.path.dirname(os.path.abspath(__file__))

#     # 最後に実行した日のデータを保存するファイルパス
#     last_execution_file = os.path.join(script_directory, 'last_execution_date.txt')

#     while True:
#         # 前回の実行日を読み込む
#         try:
#             with open(last_execution_file, 'r') as file:
#                 last_execution_date_str = file.read().strip()
#                 last_execution_date = datetime.strptime(last_execution_date_str, '%Y-%m-%d').date()
#         except FileNotFoundError:
#             # ファイルが存在しない場合は初回実行とみなし、昨日の日付を設定
#             last_execution_date = datetime.now().date() - timedelta(days=1)

#         # 現在の日付を取得
#         current_date = datetime.now().date()

#         # 日付が変わった場合のみスクレイピングとデータベース挿入を行う
#         if current_date > last_execution_date:
#             scrape_and_insert()

#             # 実行日を更新
#             with open(last_execution_file, 'w') as file:
#                 file.write(current_date.strftime('%Y-%m-%d'))

#         # 次の日まで待機
#         time.sleep(86400)  # 1日ごとに実行（24時間） 

# # 定期的に実行
while True:
    scrape_and_insert()
    time.sleep(60)  # 1時間ごとに実行

# 定期的に実行
# if __name__ == "__main__":
#     scrape_and_insert()

# import os

# スクリプトの絶対パスを取得
# script_path = os.path.abspath(__file__)

# # スクリプトのあるディレクトリの絶対パスを取得
# script_directory = os.path.dirname(script_path)

# スクリプトの絶対パスとディレクトリの絶対パスを表示
# print("Script Path:", script_path)
# print("Script Directory:", script_directory)
