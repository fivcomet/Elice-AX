# 선형회귀: 전용면적+층+건축년도+자치구(원핫) vs 비교용 전용면적 단일 모델
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CLEAN)
y = df["거래금액_만원"]

X_full = pd.concat(
    [df[["전용면적", "층", "건축년도"]],
     pd.get_dummies(df["자치구명"], prefix="자치구", drop_first=True)],
    axis=1,
)
X_area = df[["전용면적"]]

idx_tr, idx_te = train_test_split(df.index, test_size=0.3, random_state=42)

results = {}
for name, X in [("전용면적만", X_area), ("전체 특성", X_full)]:
    model = LinearRegression().fit(X.loc[idx_tr], y.loc[idx_tr])
    pred = model.predict(X.loc[idx_te])
    results[name] = (
        r2_score(y.loc[idx_te], pred),
        mean_absolute_error(y.loc[idx_te], pred),
    )
    print(f"[{name}] R² = {results[name][0]:.4f}  MAE = {results[name][1]:,.0f}만원")

print("\n테스트 30% =", len(idx_te), "건 / 학습 70% =", len(idx_tr), "건")
