import pymysql
import requests
import csv
from bs4 import BeautifulSoup

# 1. URL 수정 (page= 부분 제거)
url_base = "https://finance.naver.com/sise/nxt_sise_market_sum.naver?&page="

# 4. 헤더 추가
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

filename = "코스피_시가총액1-50위.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # newline=""은 엔터 방지
writer = csv.writer(f)

# 3. title 수정 (split() 사용)
# (가독성을 위해 불필요한 공백 제거)
title = "N 종목명 현재가 전일비 등락률 거래량 거래대금 매수호가 매도호가 시가총액".split()
writer.writerow(title)

# 2. 루프 범위 수정 (range(1, 2)로 변경 -> 1페이지만 실행)
# 만약 1~2페이지를 원한다면 range(1, 3)으로 변경
for page in range(1, 2):
    # URL 조합 및 헤더 적용
    res = requests.get(url_base + str(page), headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    data_rows = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        
        # 중간의 빈 줄(colspan) 스킵
        if len(columns) <= 1: 
            continue
            
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data)

# 파일 닫기
f.close()

print(f"'{filename}' 파일 저장 완료")