import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
1. 크롬 드라이버를 이용해 크롬 브라우저를 실행한다.
2. 메인 홈페이지에 접속
3. 닉네임을 추출, 닉네임으로 csv 생성
"""
'''
1. 닉네임에 해당하는 url로 접속
2. lastes entry 존재 시 접속.
3. 정보 추출 후 닉네임으로 된 csv 생성
4. 다음 닉네임으로 넘어가기.
'''

duple_list=[12,14,16,18,87,43,28]

# 크롬 드라이버 경로 설정
chrome_driver_path = "./chromedriver"

# 크롬 브라우저 실행
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# 웹 페이지 접속
base_url = "https://www.opendiary.com/m/author/southernbelle1788/"

nick_name_list_csv = "nick_name_list_20230526-1920.csv"

#  현재 실행 중인 파일의 경로를 가져옴
current_path = os.path.dirname(os.path.abspath(__file__))

nick_name_list_df = pd.read_csv(os.path.join(current_path, nick_name_list_csv))
# 저장할 파일의 경로를 만듦
print("시작")
for index,row in nick_name_list_df.iterrows():

    numForBackUp=0
    if index <= 37 or (index in duple_list):
        continue
    csv_raw_data=[]
    base_url=row["URL"]
    driver.get(base_url)
    print("Base : ",base_url)
    element = driver.find_elements(By.CLASS_NAME, "entry-header")[0].find_elements(By.TAG_NAME, "h4")[0].find_elements(By.TAG_NAME, "a")[0]
    some_diary_url = element.get_attribute("href")
    driver.get(some_diary_url)
    print("Some : ",some_diary_url)
    while True:
        current_url = driver.current_url
        print("현재 페이지 URL:", current_url)

        title = ""
        content = ""
        data_string = ""
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        element = soup.find(class_='time-ago')
        if element:
            date_string= element.text.strip()
        date_obj = datetime.strptime(date_string, '%B %d, %Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        
        element = soup.find(class_='entry-title')
        if element:
            title= element.text

        element = soup.find(class_='entry-content')
        if element:
            content = element.text

        # 데이터에 현재 웹주소 추가
        csv_raw_data.append([current_url,formatted_date,title,content])
        numForBackUp=numForBackUp+1
        if numForBackUp % 50 == 0:
            df = pd.DataFrame(csv_raw_data, columns=["URL","Creation Time","Title","Content"])
            # CSV 파일에 데이터 저장
            file_path = os.path.join(current_path, "data_"+str(index)+".csv")
            current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
            df.to_csv(file_path, index=True)


        prev_button = driver.find_elements(By.CLASS_NAME, "prev")[0].find_elements(By.TAG_NAME, "a")
        next_button = driver.find_elements(By.CLASS_NAME, "next")[0].find_elements(By.TAG_NAME, "a")
        if len(prev_button) == 0:
            break
        go_url=prev_button[0].get_attribute("href")
        driver.get(go_url)

    csv_raw_data=list(reversed(csv_raw_data))

    #오른쪽으로 탐색
    cnt=0

    driver.get(some_diary_url)
    while True:
        current_url = driver.current_url
        print("현재 페이지 URL:", current_url)

        title = ""
        content = ""
        data_string = ""
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        element = soup.find(class_='time-ago')
        if element:
            date_string= element.text.strip()
        date_obj = datetime.strptime(date_string, '%B %d, %Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        
        element = soup.find(class_='entry-title')
        if element:
            title= element.text

        element = soup.find(class_='entry-content')
        if element:
            content = element.text

        # 데이터에 현재 웹주소 추가

        if cnt>0:
            csv_raw_data.append([current_url,formatted_date,title,content])
            numForBackUp=numForBackUp+1
            if numForBackUp % 50 == 0:
                df = pd.DataFrame(csv_raw_data, columns=["URL","Creation Time","Title","Content"])
                # CSV 파일에 데이터 저장
                file_path = os.path.join(current_path, "data_"+str(index)+".csv")
                current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
                df.to_csv(file_path, index=True)
        cnt=cnt+1


        prev_button = driver.find_elements(By.CLASS_NAME, "prev")[0].find_elements(By.TAG_NAME, "a")
        next_button = driver.find_elements(By.CLASS_NAME, "next")[0].find_elements(By.TAG_NAME, "a")
        if len(next_button) == 0:
            break
        go_url=next_button[0].get_attribute("href")
        driver.get(go_url)

    # 브라우저 종료
    

    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(csv_raw_data, columns=["URL","Creation Time","Title","Content"])

    # CSV 파일에 데이터 저장
    file_path = os.path.join(current_path, "data_"+str(index)+".csv")
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    df.to_csv(file_path, index=True)
driver.quit()