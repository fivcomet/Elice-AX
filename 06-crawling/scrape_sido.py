import csv
import re

import requests
from bs4 import BeautifulSoup

URL = "https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def clean(text: str) -> str:
    # 각주 표기([1], [a] 등)와 양쪽 공백 제거
    return re.sub(r"\s*\[\s*[가-힣a-zA-Z]+\s*\]", "", text).strip()


response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")
table = soup.select("table.wikitable")[0]  # 남한 시·도 표

rows = []
for tr in table.select("tr"):
    cells = [clean(c.get_text(" ", strip=True)) for c in tr.find_all(["th", "td"])]
    if not cells or cells[0] == "행정 구역":
        continue  # 헤더 행 제외
    rows.append(cells[:3])  # 행정 구역, 넓이 (km²), 인구 (명)

with open("sido.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["행정 구역", "넓이 (km²)", "인구 (명)"])
    writer.writerows(rows)

print(f"{len(rows)} rows saved to sido.csv")
