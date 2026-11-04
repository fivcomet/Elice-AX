# 건축년도 / 취소일 열 점검
import pandas as pd
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CSV = os.path.join(BASE, "서울_아파트_실거래가_2025.csv")  # 원본 데이터
df = pd.read_csv(CSV)

print("=== 건축년도 ===")
y = df["건축년도"]
print("빈칸:", y.isna().sum(), "건 / 전체", len(df))
print("범위:", y.min(), "~", y.max())
print("2026 초과:", (y > 2026).sum(), "건 / 1960 미만:", (y < 1960).sum(), "건")
print(df[y.isna()].to_string())

print("\n=== 취소일 ===")
c = df["취소일"]
print("빈칸:", c.isna().sum(), "건 / 값 있음:", c.notna().sum(), "건")
cv = c.dropna().astype(int)
print("범위:", cv.min(), "~", cv.max())
# YYYYMMDD 형식 검사
month = cv // 100 % 100
day = cv % 100
print("월 1~12 벗어남:", ((month < 1) | (month > 12)).sum(), "건 / 일 1~31 벗어남:", ((day < 1) | (day > 31)).sum(), "건")
# 취소일이 계약일보다 빠른 경우
d = df.dropna(subset=["취소일"]).copy()
d["계약일"] = d["계약일"].astype(int)
d["취소일"] = d["취소일"].astype(int)
bad = d[d["취소일"] < d["계약일"]]
print("취소일 < 계약일:", len(bad), "건")
print(d["계약일"].eq(d["취소일"]).sum(), "건은 계약일과 같은 날")
