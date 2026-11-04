# 처음 보는 아파트 단지에 대한 성능 확인 (이전 모델 vs 최종 모델)
# 07·08번은 거래를 무작위로 70:30 나눠서, 같은 단지의 다른 거래가 학습과 테스트에 함께 들어갈 수 있다.
# 여기서는 단지(자치구+법정동+아파트명) 단위로 나눠, 학습에 한 번도 없던 단지만으로 테스트한다.
import os
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

BASE = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CLEAN)
df["계약일수"] = (pd.to_datetime(df["계약일"].astype(str), format="%Y%m%d")
                  - pd.to_datetime("20241115", format="%Y%m%d")).dt.days
y = df["거래금액_만원"]

X_old = pd.concat(
    [df[["전용면적", "층", "건축년도", "계약일수"]],
     pd.get_dummies(df[["자치구명", "신고구분"]], drop_first=True)],
    axis=1,
)
X_new = pd.concat(
    [X_old, pd.get_dummies(df["자치구명"] + " " + df["법정동명"], prefix="동", drop_first=True)],
    axis=1,
)
단지 = df["자치구명"] + "_" + df["법정동명"] + "_" + df["아파트명"]
idx_tr, idx_te = next(GroupShuffleSplit(test_size=0.3, random_state=42).split(X_old, y, 단지))
print(f"단지 수: {단지.nunique():,}개 (테스트 단지는 학습에 없음)")

for name, X, n, leaf in [("이전 모델 (나무 200, 최소 2건)", X_old, 200, 2),
                         ("최종 모델 (+법정동, 나무 50, 최소 5건)", X_new, 50, 5)]:
    model = RandomForestRegressor(n_estimators=n, min_samples_leaf=leaf,
                                  n_jobs=-1, random_state=42).fit(X.iloc[idx_tr], y.iloc[idx_tr])
    pred = model.predict(X.iloc[idx_te])
    print(f"{name:<32} R² = {r2_score(y.iloc[idx_te], pred):.4f}  "
          f"MAE = {mean_absolute_error(y.iloc[idx_te], pred):,.0f}만원")
