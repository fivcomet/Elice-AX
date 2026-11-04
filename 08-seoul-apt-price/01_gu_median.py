# 자치구별 아파트 거래금액(만원) 중앙값 막대그래프
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
OUT = os.path.join(BASE, "gu_price.png")

df = pd.read_csv(CSV)

# 취소된 거래는 실제 가격이 아니므로 제외
df = df[df["취소일"].isna()]

med = (
    df.groupby("자치구명")["거래금액_만원"]
    .median()
    .sort_values(ascending=False)
)
print(med)

fig, ax = plt.subplots(figsize=(12, 6))
med.plot(kind="bar", ax=ax, color="#3b6ea5")
ax.set_title("서울 자치구별 아파트 거래금액 중앙값 (2025, 만원)", fontsize=14)
ax.set_xlabel("자치구")
ax.set_ylabel("거래금액 중앙값 (만원)")
ax.tick_params(axis="x", rotation=45)
for label in ax.get_xticklabels():
    label.set_ha("right")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print("saved:", OUT, f"(취소 제외 거래 {len(df):,}건)")
