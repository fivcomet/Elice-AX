# 모델 경량화 실험: 나무 수·잎 최소 크기·법정동 특성에 따라 용량과 성능이 어떻게 바뀌는지 비교
# 결과: 용량은 특성 수가 아니라 나무의 크기(가지 수)가 결정한다.
#       잎을 잘게(최소 2건) 나누면 기존 방식 점수는 오르지만, 처음 보는 단지 점수는 그대로다 → 외운 부분
import os
import tempfile
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

BASE = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")

df = pd.read_csv(CLEAN)
df["계약일수"] = (pd.to_datetime(df["계약일"].astype(str), format="%Y%m%d")
                  - pd.to_datetime("20241115", format="%Y%m%d")).dt.days
y = df["거래금액_만원"]
X_base = pd.concat(
    [df[["전용면적", "층", "건축년도", "계약일수"]],
     pd.get_dummies(df[["자치구명", "신고구분"]], drop_first=True)],
    axis=1,
)
X_dong = pd.concat(
    [X_base, pd.get_dummies(df["자치구명"] + " " + df["법정동명"], prefix="동", drop_first=True)],
    axis=1,
)

idx_tr, idx_te = train_test_split(df.index, test_size=0.3, random_state=42)          # 거래 단위 무작위 분할
단지 = df["자치구명"] + "_" + df["법정동명"] + "_" + df["아파트명"]
g_tr, g_te = next(GroupShuffleSplit(test_size=0.3, random_state=42).split(X_base, y, 단지))  # 단지 단위 분할

def model_size_mb(model):
    """모델을 압축 저장했을 때의 파일 크기(MB)"""
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "m.joblib")
        joblib.dump(model, path, compress=3)
        return os.path.getsize(path) / 1e6

settings = [
    ("기존",       X_base, 200, 2),
    ("기존",       X_base, 100, 2),
    ("기존",       X_base,  50, 5),
    ("+법정동",    X_dong,  50, 5),   # 최종 선택
]
print(f"{'특성':<8}{'나무':>5}{'최소':>5}{'용량':>9}{'R²(무작위)':>12}{'MAE':>11}{'R²(새 단지)':>13}")
for name, X, n, leaf in settings:
    m = RandomForestRegressor(n_estimators=n, min_samples_leaf=leaf, n_jobs=-1, random_state=42)
    m.fit(X.loc[idx_tr], y.loc[idx_tr])
    p = m.predict(X.loc[idx_te])
    size = model_size_mb(m)
    m2 = RandomForestRegressor(n_estimators=n, min_samples_leaf=leaf, n_jobs=-1, random_state=42)
    p2 = m2.fit(X.iloc[g_tr], y.iloc[g_tr]).predict(X.iloc[g_te])
    print(f"{name:<8}{n:>5}{leaf:>5}{size:>7.1f}MB{r2_score(y.loc[idx_te], p):>12.4f}"
          f"{mean_absolute_error(y.loc[idx_te], p):>10,.0f}만{r2_score(y.iloc[g_te], p2):>13.4f}")
