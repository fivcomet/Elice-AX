import csv

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

response = requests.get(URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

rows = []
for article in soup.select("article.product_pod"):
    title = article.select_one("h3 a")["title"]
    price = article.select_one("p.price_color").get_text(strip=True)
    rows.append([title, price])

with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "price"])
    writer.writerows(rows)

print(f"{len(rows)} books saved to books.csv")
