import time
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

nick_name_list_csv = "nick_name_list_20230526-1920.csv"

#  현재 실행 중인 파일의 경로를 가져옴
current_path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(current_path, nick_name_list_csv)).drop('Unnamed: 0', axis=1)

print(df)

# 중복된 행 제거
df_no_duplicates = df.drop_duplicates(subset=['Nickname'])

# 수정된 데이터 저장
df_no_duplicates.to_csv('nick_name_list_20230527-0232.csv',index=True)
print("AAA")

while(True):
    pass

def getNickNameFromHTML(html):
    soup = BeautifulSoup(html, 'html.parser')
    nick_name_list = []
    for div in soup.find_all(class_='author-name'):
        if div:
            for a in div.find_all('a'):
                if a and [a.text,a['href']] not in nick_name_list:
                    nick_name_list.append([a.text,a['href']])
    return nick_name_list


# 크롬 드라이버 경로 설정
chrome_driver_path = "./chromedriver"

# 크롬 브라우저 실행
driver = webdriver.Chrome(executable_path=chrome_driver_path)

base_url = "https://www.opendiary.com/"
driver.get(base_url)
minTargetExtractNum = 500
nick_name_list = []
targetScreenHeight = 0
while(len(nick_name_list)<minTargetExtractNum):
    currentScreenHeight = driver.execute_script("return window.screen.height;")
    targetScreenHeight += currentScreenHeight
    driver.execute_script("window.scrollTo(0, {x});".format(x=targetScreenHeight))
    while driver.execute_script("return document.body.scrollHeight;") < targetScreenHeight:
        driver.execute_script("window.scrollTo(0, {x});".format(x=targetScreenHeight))
        time.sleep(0.2)
    nick_name_list=getNickNameFromHTML(driver.page_source)
    print("현재 추출된 닉네임 수:",len(nick_name_list))

driver.quit()

# 데이터를 DataFrame으로 변환
df = pd.DataFrame(nick_name_list, columns=["Nickname", "URL"])

# CSV 파일에 데이터 저장
# 현재 시간 얻기
current_time = datetime.now().strftime("%Y%m%d-%H%M")
#  현재 실행 중인 파일의 경로를 가져옴
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, f"nick_name_list_{current_time}.csv")
df.to_csv(file_path, index=True)
