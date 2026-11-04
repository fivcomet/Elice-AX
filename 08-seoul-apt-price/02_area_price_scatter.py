# 전용면적 vs 거래금액 산점도
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

import os

# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

# 한글 폰트 설정 (윈도우: 맑은 고딕 / 맥: 애플고딕 / 리눅스: 나눔고딕 중 있는 것 사용)
_installed = {f.name for f in fm.fontManager.ttflist}
for _p in ["/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
    if os.path.exists(_p):
        fm.fontManager.addfont(_p)
        _installed.add(fm.FontProperties(fname=_p).get_name())
for _name in ["Malgun Gothic", "AppleGothic", "NanumGothic", "Noto Sans CJK KR"]:
    if _name in _installed:
        plt.rc("font", family=_name)
        break
plt.rcParams["axes.unicode_minus"] = False

CSV = os.path.join(BASE, "서울_아파트_실거래가_2025.csv")  # 원본 데이터
OUT = os.path.join(BASE, "area_price.png")

df = pd.read_csv(CSV)
df = df[df["취소일"].isna()]

corr = df["전용면적"].corr(df["거래금액_만원"])
print(f"상관계수: {corr:.3f}, 거래 {len(df):,}건")

fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(df["전용면적"], df["거래금액_만원"], s=4, alpha=0.15, color="#3b6ea5", edgecolors="none")
ax.set_title(f"서울 아파트 전용면적 vs 거래금액 (2025, 취소 제외 {len(df):,}건)\n상관계수 r = {corr:.3f}", fontsize=13)
ax.set_xlabel("전용면적 (㎡)")
ax.set_ylabel("거래금액 (만원)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print("saved:", OUT)
