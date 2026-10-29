# 06. 웹 크롤링

🔗 **[대시보드 열기](https://fivcomet.github.io/Elice-AX/06-crawling/dashboard.html)**

`requests`와 `BeautifulSoup`으로 웹페이지에서 데이터를 수집해 CSV로 저장하고, 그 데이터로 시각화한 실습입니다.

## 파일

| 파일 | 설명 |
|---|---|
| [`scrape_books.py`](https://github.com/fivcomet/Elice-AX/blob/main/06-crawling/scrape_books.py) | 크롤링 연습 사이트(books.toscrape.com) Mystery 분야의 책 제목과 가격 수집 → `books.csv` |
| [`books.csv`](https://github.com/fivcomet/Elice-AX/blob/main/06-crawling/books.csv) | 수집 결과 (20권) |
| [`scrape_sido.py`](https://github.com/fivcomet/Elice-AX/blob/main/06-crawling/scrape_sido.py) | 위키백과 「대한민국의 행정 구역」 표에서 시·도별 넓이와 인구 수집 → `sido.csv` |
| [`sido.csv`](https://github.com/fivcomet/Elice-AX/blob/main/06-crawling/sido.csv) | 수집 결과 (16개 시·도 + 합계) |
| [`dashboard.html`](https://github.com/fivcomet/Elice-AX/blob/main/06-crawling/dashboard.html) | `sido.csv`로 만든 「사람이 가장 빽빽하게 사는 시·도는?」 대시보드 |

## 결과

서울특별시의 인구밀도는 1km²당 약 16,144명으로, 2위 부산(약 4,463명)의 3.6배, 전국 평균(약 516명)의 31배입니다.

## 실행 방법

```bash
pip install requests beautifulsoup4
python scrape_books.py
python scrape_sido.py
```

CSV는 엑셀에서 한글이 깨지지 않도록 `utf-8-sig`로 저장합니다.
