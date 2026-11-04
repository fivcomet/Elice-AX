# 추천 기법 비교: 로그 타겟 선형회귀 vs 랜덤포레스트 vs 그래디언트부스팅
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CLEAN)
df["계약일수"] = (pd.to_datetime(df["계약일"].astype(str), format="%Y%m%d")
                  - pd.to_datetime("20241115", format="%Y%m%d")).dt.days

y = df["거래금액_만원"]
X = pd.concat(
    [df[["전용면적", "층", "건축년도", "계약일수"]],
     pd.get_dummies(df[["자치구명", "신고구분"]], drop_first=True)],
    axis=1,
)

idx_tr, idx_te = train_test_split(df.index, test_size=0.3, random_state=42)
X_tr, X_te = X.loc[idx_tr], X.loc[idx_te]
y_tr, y_te = y.loc[idx_tr], y.loc[idx_te]

def report(name, pred):
    print(f"{name:<22} R² = {r2_score(y_te, pred):.4f}  "
          f"MAE = {mean_absolute_error(y_te, pred):,.0f}만원")
    return r2_score(y_te, pred), mean_absolute_error(y_te, pred)

# 1) 선형회귀 (기존 ③과 동일)
pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)
report("① 선형회귀", pred)

# 2) 로그 타겟 선형회귀
m = LinearRegression().fit(X_tr, np.log1p(y_tr))
report("② 로그 타겟 선형회귀", np.expm1(m.predict(X_te)))

# 3) 랜덤포레스트
m = RandomForestRegressor(n_estimators=200, min_samples_leaf=2,
                          n_jobs=-1, random_state=42).fit(X_tr, y_tr)
report("③ 랜덤포레스트", m.predict(X_te))
imp = pd.Series(m.feature_importances_, index=X.columns).sort_values(ascending=False)
print("   중요 특성 TOP5:", ", ".join(f"{k} {v:.2f}" for k, v in imp.head(5).items()))

# 4) 히스토그램 그래디언트부스팅
m = HistGradientBoostingRegressor(random_state=42).fit(X_tr, y_tr)
report("④ 그래디언트부스팅", m.predict(X_te))
