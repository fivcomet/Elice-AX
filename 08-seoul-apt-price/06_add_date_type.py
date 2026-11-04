# 계약일(경과 일수), 신고구분(원핫) 추가 모델과 이전 모델 비교
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CLEAN)
df["계약일"] = pd.to_datetime(df["계약일"].astype(str), format="%Y%m%d")
df["계약일수"] = (df["계약일"] - df["계약일"].min()).dt.days  # 2024-11-15 = 0

y = df["거래금액_만원"]
dummies = pd.get_dummies(df[["자치구명", "신고구분"]], drop_first=True)

X_area = df[["전용면적"]]
X_prev = pd.concat([df[["전용면적", "층", "건축년도"]],
                    pd.get_dummies(df["자치구명"], prefix="자치구", drop_first=True)], axis=1)
X_new = pd.concat([X_prev, df[["계약일수"]], dummies[["신고구분_직거래"]]], axis=1)

idx_tr, idx_te = train_test_split(df.index, test_size=0.3, random_state=42)

for name, X in [("① 전용면적만", X_area),
                ("② +층,건축년도,자치구", X_prev),
                ("③ ② +계약일,신고구분", X_new)]:
    model = LinearRegression().fit(X.loc[idx_tr], y.loc[idx_tr])
    pred = model.predict(X.loc[idx_te])
    print(f"{name}  R² = {r2_score(y.loc[idx_te], pred):.4f}  "
          f"MAE = {mean_absolute_error(y.loc[idx_te], pred):,.0f}만원")

# 계약일수 계수(일별 금액 변화)
m = LinearRegression().fit(X_new.loc[idx_tr], y.loc[idx_tr])
print("\n계약일수 계수:", round(m.coef_[X_new.columns.get_loc("계약일수")], 1), "만원/일")
print("신고구분_직거래 계수:", round(m.coef_[X_new.columns.get_loc("신고구분_직거래")], 1), "만원")
