# 최종 모델 학습 후 저장 (다른 PC에서 불러 쓰기용)
# 11_model_diet.py 비교 결과로 최종 설정을 바꿨다:
#   - 법정동 특성 추가 (처음 보는 단지 성능 R² 0.67 → 0.79)
#   - 나무 200 → 50그루, 잎(마지막 가지)의 최소 거래 수 2 → 5 (모델 파일 100MB → 약 11MB)
import sklearn
import joblib
import pandas as pd
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import os
# 이 파이썬 파일이 있는 폴더 (어디서 실행해도 같은 폴더의 파일을 찾도록)
BASE = os.path.dirname(os.path.abspath(__file__))

CLEAN = os.path.join(BASE, "서울_아파트_실거래가_2025_clean.csv")
OUT = os.path.join(BASE, "rf_model.joblib")

df = pd.read_csv(CLEAN)
df["계약일수"] = (pd.to_datetime(df["계약일"].astype(str), format="%Y%m%d")
                  - pd.to_datetime("20241115", format="%Y%m%d")).dt.days

X = pd.concat(
    [df[["전용면적", "층", "건축년도", "계약일수"]],
     pd.get_dummies(df[["자치구명", "신고구분"]], drop_first=True),
     # 법정동: 구가 달라도 이름이 같은 동이 있어 "자치구 법정동"으로 묶어 원핫 인코딩
     pd.get_dummies(df["자치구명"] + " " + df["법정동명"], prefix="동", drop_first=True)],
    axis=1,
)
y = df["거래금액_만원"]
idx_tr, idx_te = train_test_split(df.index, test_size=0.3, random_state=42)

model = RandomForestRegressor(n_estimators=50, min_samples_leaf=5,
                              n_jobs=-1, random_state=42).fit(X.loc[idx_tr], y.loc[idx_tr])
pred = model.predict(X.loc[idx_te])
print(f"저장 전 확인: R² = {r2_score(y.loc[idx_te], pred):.4f}, "
      f"MAE = {mean_absolute_error(y.loc[idx_te], pred):,.0f}만원")

# 모델 + 특성 목록 + 환경 정보를 한 파일에 저장
bundle = {
    "model": model,
    "feature_columns": list(X.columns),
    "dong_list": sorted((df["자치구명"] + " " + df["법정동명"]).unique()),  # 학습에 있던 법정동 목록
    "sklearn_version": sklearn.__version__,
    "trained_on": str(date.today()),
    "test_r2": r2_score(y.loc[idx_te], pred),
    "test_mae": mean_absolute_error(y.loc[idx_te], pred),
}
joblib.dump(bundle, OUT, compress=3)  # 압축 저장 (파일 용량 절약)
print("saved:", OUT)
