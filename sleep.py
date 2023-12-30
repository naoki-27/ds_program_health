import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import sqlite3
import os

def scrape_and_insert():
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
    print(sleep_dict)

    # データベースへの挿入
    path = '/Users/naoki/Lecture/ds_program_health/'
    db_name = 'sleep.sqlite'
    con = sqlite3.connect(path + db_name)
    cur = con.cursor()

    sql_insert_data = 'INSERT INTO sleep (date, sleep_point, high_temperature, low_temperature, precip, weather, coment) VALUES (?, ?, ?, ?, ?, ?, ?);'
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

scrape_and_insert()