# 데이터 정제: 취소 거래 + 건축년도 이상치(0, NaN) 제외
import pandas as pd
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CSV = os.path.join(BASE, "서울_아파트_실거래가_2025.csv")  # 원본 데이터
OUT = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CSV)
n0 = len(df)

df = df[df["취소일"].isna()]
n1 = len(df)

df = df[(df["건축년도"].notna()) & (df["건축년도"] > 1900)]
n2 = len(df)

df.to_csv(OUT, index=False)

print(f"원본 {n0:,}건")
print(f"- 취소일 있는 거래 제외 {n0 - n1:,}건 → {n1:,}건")
print(f"- 건축년도 0/빈칸 제외 {n1 - n2:,}건 → 최종 {n2:,}건")
print(f"빈칸 남은 열:\n{df.isna().sum()[df.isna().sum() > 0]}")
print("saved:", OUT)
