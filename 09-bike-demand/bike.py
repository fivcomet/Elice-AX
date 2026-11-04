# ============================================================
# 따릉이 대여량 데이터 분석 + 수요 예측 모델
# (모든 줄에 초보자용 주석 / 이슬점은 특성에서 제외)
# ============================================================

import pandas as pd    # 엑셀처럼 생긴 표(데이터프레임)를 다루는 라이브러리 pandas를 불러옵니다
import numpy as np     # 로그 등 숫자 계산에 쓰는 라이브러리 numpy를 불러옵니다
import os              # 파일 경로를 다루는 도구 os를 불러옵니다

BASE = os.path.dirname(os.path.abspath(__file__))   # 이 파이썬 파일이 있는 폴더 경로 (어디서 실행해도 같은 폴더의 파일을 찾도록)

# ── 1. 데이터 읽기 ──
df = pd.read_csv(os.path.join(BASE, '따릉이_대여량.csv'), encoding='utf-8-sig')   # CSV 파일을 읽어 'df'라는 이름의 표로 만듭니다

# ── 2. 행/열 개수 세기 ──
print(f"행 개수: {df.shape[0]}")   # df.shape[0]은 표의 줄(행) 개수입니다
print(f"열 개수: {df.shape[1]}")   # df.shape[1]은 표의 칸(열) 개수입니다

# ── 3. 열별 자료형 확인 (숫자인지 글자인지) ──
print("\n[열 자료형 요약]")                                    # 제목을 출력합니다
result = []                                                    # 각 열의 정보를 차곡차곡 담을 빈 목록을 만듭니다
for col in df.columns:                                         # 표의 모든 열 이름을 하나씩 꺼내며 반복합니다
    dtype = df[col].dtype                                      # 그 열에 저장된 값의 자료형(숫자/글자 등)을 확인합니다
    kind = '숫자' if pd.api.types.is_numeric_dtype(df[col]) else '글자'   # 숫자형이면 '숫자', 아니면 '글자'로 분류합니다
    result.append({'열 이름': col, 'pandas 자료형': str(dtype), '구분': kind})   # 열 이름·자료형·구분을 한 세트로 묶어 목록에 추가합니다

type_df = pd.DataFrame(result)                 # 목록을 다시 표(데이터프레임)로 만듭니다
print(type_df.to_string(index=False))          # 표를 줄번호 없이 출력합니다

# ── 4. 시간대별 평균 대여건수 막대그래프 ──
import matplotlib.pyplot as plt                # 그래프를 그리는 라이브러리 matplotlib을 불러옵니다
from matplotlib import font_manager as fm      # 컴퓨터에 설치된 폰트 목록을 확인하는 도구를 불러옵니다
installed = {f.name for f in fm.fontManager.ttflist}   # 설치된 폰트 이름들을 모읍니다
for font in ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR']:   # 윈도우·맥·리눅스용 한글 폰트를 차례로 확인합니다
    if font in installed:                      # 그 폰트가 설치되어 있으면
        plt.rcParams['font.family'] = font     # 그래프 글꼴로 지정하고
        break                                  # 더 찾지 않고 멈춥니다
plt.rcParams['axes.unicode_minus'] = False     # 마이너스(-) 기호가 깨지는 현상을 막습니다

hourly_mean = df.groupby('시간')['대여건수'].mean()   # 같은 시간끼리 묶어 대여건수 평균을 계산합니다 (0시~23시)

plt.figure(figsize=(10, 5))                    # 가로 10, 세로 5 크기의 도화지를 준비합니다
plt.bar(hourly_mean.index, hourly_mean.values, color='steelblue', edgecolor='black')   # 시간대별 평균값으로 막대그래프를 그립니다
plt.title('시간대별 평균 대여건수')             # 그래프 제목을 붙입니다
plt.xlabel('시간')                             # x축 이름을 붙입니다
plt.ylabel('평균 대여건수')                     # y축 이름을 붙입니다
plt.xticks(range(0, 24))                       # x축에 0부터 23까지 모두 표시합니다
plt.grid(axis='y', alpha=0.3)                  # y축 방향으로 옅은 눈금선을 깔아 읽기 쉽게 합니다
plt.tight_layout()                             # 글자가 잘리지 않게 여백을 자동 조절합니다
plt.savefig(os.path.join(BASE, 'bike_hour.png'), dpi=150)   # 그래프를 bike_hour.png 파일로 저장합니다
plt.close()                                    # 도화지를 닫아 메모리를 정리합니다
print("\nbike_hour.png 저장 완료")              # 저장이 끝났다고 알려줍니다

# ── 5. 터미널에서 바로 보는 텍스트 그래프 ──
print("\n[시간대별 평균 대여건수 - 텍스트 그래프]")   # 제목을 출력합니다
max_val = hourly_mean.max()                    # 시간대별 평균 중 가장 큰 값을 찾습니다 (막대 길이의 기준)
for hour, mean in hourly_mean.items():         # 시간과 평균값을 하나씩 꺼내며 반복합니다
    bar = '█' * round(mean / max_val * 40)     # 평균이 클수록 네모(█)를 많이 이어 긴 막대를 만듭니다
    print(f"{hour:2d}시 {bar} {mean:6.0f}")    # 시간, 막대, 평균값을 한 줄에 출력합니다

# ── 6. 비가 안 올 때 vs 올 때 평균 대여건수 비교 ──
no_rain = df.loc[df['강수량'] == 0, '대여건수']   # 강수량이 0인 줄의 대여건수만 골라냅니다
rain = df.loc[df['강수량'] > 0, '대여건수']       # 강수량이 0보다 큰 줄의 대여건수만 골라냅니다

print("\n[강수량에 따른 평균 대여건수 비교]")   # 제목을 출력합니다
print(f"강수량 = 0     : {no_rain.mean():.1f}건  ({len(no_rain)}시간)")   # 비 안 온 시간의 평균과 개수를 출력합니다
print(f"강수량 > 0     : {rain.mean():.1f}건  ({len(rain)}시간)")         # 비 온 시간의 평균과 개수를 출력합니다
print(f"차이           : {no_rain.mean() - rain.mean():.1f}건 "                 # 두 평균의 차이를 출력하고
      f"(비 올 때 {(1 - rain.mean() / no_rain.mean()) * 100:.1f}% 감소)")       # 비가 올 때 몇 % 줄었는지도 출력합니다
op = df[df['운영일'] == '운영']                   # 서비스가 운영된 시간만 골라냅니다 (미운영 시간은 대여 0건이라 평균을 낮춤)
op_no, op_rain = op.loc[op['강수량'] == 0, '대여건수'], op.loc[op['강수량'] > 0, '대여건수']   # 운영 시간 중 비 안 온/온 시간을 나눕니다
print(f"(운영 시간만: {op_no.mean():.1f}건 → {op_rain.mean():.1f}건, "            # 운영 시간만으로 다시 비교하고
      f"{(1 - op_rain.mean() / op_no.mean()) * 100:.1f}% 감소)")                 # 감소율을 출력합니다

# ── 7. 비 온 시간만 모아 강수량 '양'에 따른 대여건수 비교 ──
rain_df = df[df['강수량'] > 0].copy()   # 강수량이 0보다 큰 줄만 따로 복사해 둡니다

# 7-1. 스케일링(값의 크기를 다시 잡기)
rain_df['강수량_minmax'] = (rain_df['강수량'] - rain_df['강수량'].min()) / (rain_df['강수량'].max() - rain_df['강수량'].min())   # 최소를 0, 최대를 1로 만드는 MinMax 계산
rain_df['강수량_log'] = np.log1p(rain_df['강수량'])   # 로그를 씌워 큰 값의 치우침을 줄입니다

print("\n[강수량(>0) 분포 요약]")                           # 제목을 출력합니다
print(rain_df['강수량'].describe().round(2).to_string())   # 평균·최소·최대 등 요약통계를 소수점 2자리로 출력합니다

print("\n[스케일링 전후 상관계수 vs 대여건수]")   # 제목을 출력합니다
print(f"원본 강수량      : Pearson {rain_df['강수량'].corr(rain_df['대여건수']):.3f}, "   # 원본 값과 대여건수의 상관계수를 출력하고
      f"Spearman {rain_df['강수량'].corr(rain_df['대여건수'], method='spearman'):.3f}")   # 순위 기반 상관계수도 함께 출력합니다
print(f"log1p 강수량     : Pearson {rain_df['강수량_log'].corr(rain_df['대여건수']):.3f}")   # 로그 변환 후 상관계수가 나아지는지 봅니다
print(f"MinMax 강수량    : Pearson {rain_df['강수량_minmax'].corr(rain_df['대여건수']):.3f} (스케일만 변하므로 원본 Pearson과 동일)")   # MinMax는 크기만 바꾸므로 상관계수가 같음을 확인합니다

# 7-2. 강수량을 구간으로 나눠 평균 비교
bins = [0, 1, 3, 6, 10, 100]                                  # 구간의 경계값들 (0~1, 1~3, 3~6, 6~10, 10~100mm)
labels = ['0~1mm', '1~3mm', '3~6mm', '6~10mm', '10mm 이상']   # 각 구간의 이름표
rain_df['강수량_구간'] = pd.cut(rain_df['강수량'], bins=bins, labels=labels)   # 강수량 값을 구간 이름으로 바꿔 새 열에 넣습니다
summary = rain_df.groupby('강수량_구간')['대여건수'].agg(평균='mean', 데이터수='count').round(1)   # 구간별 평균과 개수를 한 번에 계산합니다
print("\n[강수량 구간별 평균 대여건수]")   # 제목을 출력합니다
print(summary.to_string())                # 구간별 요약표를 출력합니다

# ── 8. 계절별 평균 대여건수 (많은 순서) ──
season_mean = df.groupby('계절')['대여건수'].mean().sort_values(ascending=False)   # 계절별 평균을 구해 큰 순서로 정렬합니다
print("\n[계절별 평균 대여건수 - 내림차순]")   # 제목을 출력합니다
max_season = season_mean.max()                 # 계절 평균 중 최댓값 (막대 길이의 기준)
for season, mean in season_mean.items():       # 계절과 평균값을 하나씩 꺼내며 반복합니다
    bar = '█' * round(mean / max_season * 40)  # 평균에 비례해 텍스트 막대를 만듭니다
    print(f"{season}: {bar} {mean:.1f}건")     # 계절, 막대, 평균을 출력합니다

# ── 9. 평일 vs 휴일 평균 대여건수 비교 ──
holiday_mean = df.groupby('휴일')['대여건수'].agg(['mean', 'count'])   # 휴일 값별로 평균(mean)과 개수(count)를 계산합니다
print("\n[휴일 여부별 평균 대여건수]")          # 제목을 출력합니다
for name, row in holiday_mean.iterrows():      # 휴일 값별 결과를 한 줄씩 꺼내며 반복합니다
    print(f"{name}: {row['mean']:.1f}건  ({int(row['count'])}시간)")   # 평균과 개수를 출력합니다
diff = holiday_mean['mean'].max() - holiday_mean['mean'].min()    # 평균의 차이를 계산합니다
print(f"차이: {diff:.1f}건")                   # 차이를 출력합니다

# ── 10. 대여건수가 0인 줄 찾아보기 ──
zero_df = df[df['대여건수'] == 0]              # 대여건수가 0인 줄만 골라냅니다
print(f"\n[대여건수가 0인 줄: {len(zero_df)}개]")   # 그런 줄이 몇 개인지 출력합니다
print("\n[이 줄들의 운영일 열 값 분포]")        # 제목을 출력합니다
print(zero_df['운영일'].value_counts().to_string())   # 그 줄들의 운영일 값이 무엇인지 세어 출력합니다
print("\n[참고: 운영일 값별 전체 줄 수와 0인 줄 수]")   # 제목을 출력합니다
check = df.groupby('운영일')['대여건수'].agg(전체='count', 대여건수0=lambda x: (x == 0).sum())   # 운영일 값별로 전체 줄 수와 0인 줄 수를 계산합니다
print(check.to_string())                       # 결과표를 출력합니다

# ── 11. 대여건수와 숫자 열들의 상관계수 (많은 순서 그래프) ──
corr = df.corr(numeric_only=True)['대여건수'].drop('대여건수').sort_values(ascending=False)   # 숫자 열들과 대여건수의 상관계수를 구해 큰 순서로 정렬합니다
print("\n[대여건수와 숫자 열들의 상관계수 - 내림차순]")   # 제목을 출력합니다
print(corr.round(3).to_string())               # 상관계수를 소수점 3자리로 출력합니다

plt.figure(figsize=(10, 5))                    # 가로 10, 세로 5 크기의 도화지를 준비합니다
colors = ['steelblue' if v >= 0 else 'indianred' for v in corr.values]   # 양수는 파랑, 음수는 빨강으로 칠할 색 목록을 만듭니다
plt.bar(corr.index, corr.values, color=colors, edgecolor='black')   # 열 이름별 상관계수 막대그래프를 그립니다
plt.title('대여건수와 숫자 열들의 상관계수')    # 그래프 제목을 붙입니다
plt.ylabel('상관계수')                          # y축 이름을 붙입니다
plt.axhline(0, color='black', linewidth=0.8)   # 0 기준선을 검은 가로선으로 그립니다
plt.xticks(rotation=30)                        # x축 글자를 30도 기울여 겹치지 않게 합니다
plt.grid(axis='y', alpha=0.3)                  # y축 방향 옅은 눈금선을 깝니다
plt.tight_layout()                             # 여백을 자동 조절합니다
plt.savefig(os.path.join(BASE, 'bike_corr.png'), dpi=150)   # 그래프를 bike_corr.png 파일로 저장합니다
plt.close()                                    # 도화지를 닫습니다
print("\nbike_corr.png 저장 완료")              # 저장 완료를 알려줍니다

# ── 12. 계절, 휴일 열을 원-핫 인코딩(0/1 칸)으로 바꾸기 ──
df = pd.get_dummies(df, columns=['계절', '휴일'], dtype=int)   # 글자 열(계절, 휴일)을 '해당하면 1, 아니면 0' 칸들로 바꿉니다
print(f"\n[원-핫 인코딩 후: {df.shape[1]}열]")   # 열이 몇 개로 늘었는지 출력합니다
for i, col in enumerate(df.columns, 1):        # 열 이름을 하나씩 꺼내며 번호를 붙입니다
    print(f"{i:2d}. {col}")                    # 번호와 열 이름을 출력합니다

# ── 13. 시간 열도 원-핫 인코딩(0시~23시 24칸)으로 바꾸기 ──
df = pd.get_dummies(df, columns=['시간'], dtype=int)   # 시간 열을 0~23의 24개 0/1 칸으로 바꿉니다
df = df.rename(columns={f'시간_{h}': f'시간_{h}시' for h in range(24)})   # 칸 이름을 시간_0시 ~ 시간_23시로 바꿉니다
print(f"\n[시간 원-핫 인코딩 후: {df.shape[1]}열]")   # 열 개수를 출력합니다
for i, col in enumerate(df.columns, 1):        # 열 이름을 하나씩 꺼내며 번호를 붙입니다
    print(f"{i:2d}. {col}")                    # 번호와 열 이름을 출력합니다

# ── 14. 날짜 열에서 월·요일을 뽑고, 날짜 열은 지우기 ──
df['날짜'] = pd.to_datetime(df['날짜'], dayfirst=True)   # 글자 날짜를 진짜 날짜형으로 바꿉니다 (일/월/년 순서로 읽음)
df['월'] = df['날짜'].dt.month                 # 날짜에서 월(1~12)만 뽑아 새 열로 만듭니다
df['요일'] = df['날짜'].dt.dayofweek           # 날짜에서 요일(0=월 ~ 6=일)만 뽑아 새 열로 만듭니다
day_of_month = df['날짜'].dt.day               # 며칠인지(1~31)는 특성으로 쓰지 않고, 19번 검증에만 쓰려고 따로 보관합니다
df = df.drop(columns=['날짜'])                 # 이제 필요 없어진 원래 날짜 열을 지웁니다

# ── 15. 서비스가 멈춘 시간(미운영) 지우기 + '비 여부' 만들기 ──
df = df[df['운영일'] == '운영'].drop(columns=['운영일'])   # 미운영(대여건수 0) 줄을 지우고, 판단에 쓴 운영일 열도 지웁니다
df['비 여부'] = (df['강수량'] > 0).astype(int)   # 비가 조금이라도 오면 1, 안 오면 0인 새 열을 만듭니다
print(f"\n[모델용 데이터: {df.shape[0]}행 × {df.shape[1]}열]")   # 모델 학습에 쓸 표의 크기를 출력합니다

# ── 16. 데이터를 학습용 70% / 시험용 30%로 나눠 선형회귀 학습 ──
from sklearn.model_selection import train_test_split   # 데이터를 나누는 도구를 불러옵니다
from sklearn.linear_model import LinearRegression      # 선형회귀 모델을 불러옵니다
from sklearn.metrics import r2_score, mean_absolute_error   # 성능 점수(R2, MAE)를 계산하는 도구를 불러옵니다

X = df.drop(columns=['대여건수', '이슬점'])   # 정답(대여건수)과 빼기로 한 이슬점을 제외한 나머지 열을 전부 특성(X)으로 씁니다
y = df['대여건수']                            # 맞춰야 할 정답(타겟)은 대여건수입니다
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=21)   # 전체를 70%(학습)/30%(시험)로 나눕니다 (random_state는 나누는 방식을 고정)

model = LinearRegression()                     # 선형회귀 모델을 준비합니다
model.fit(X_train, y_train)                    # 학습용 데이터로 모델을 훈련시킵니다
pred = model.predict(X_test)                   # 시험용 데이터의 대여건수를 예측해 봅니다
print("\n[선형회귀 - 전체 특성(이슬점 제외)]")   # 제목을 출력합니다
print(f"R2  : {r2_score(y_test, pred):.3f}")   # R2(설명력, 1에 가까울수록 좋음)를 출력합니다
print(f"MAE : {mean_absolute_error(y_test, pred):.1f}건")   # MAE(평균 오차, 작을수록 좋음)를 출력합니다

# ── 17. 비교용: 기온 하나만 넣은 선형회귀 ──
X_one = df[['기온']]                           # 특성을 기온 하나만 남깁니다
X1_train, X1_test, y1_train, y1_test = train_test_split(X_one, y, test_size=0.3, random_state=21)   # 같은 방식(70:30, random_state=21)으로 나눠 공정하게 비교합니다
model_one = LinearRegression()                 # 비교용 선형회귀 모델을 준비합니다
model_one.fit(X1_train, y1_train)              # 기온만으로 훈련시킵니다
pred_one = model_one.predict(X1_test)          # 시험용 데이터를 예측해 봅니다
print("\n[선형회귀 - 기온만 사용]")             # 제목을 출력합니다
print(f"R2  : {r2_score(y1_test, pred_one):.3f}")   # 기온만 쓴 모델의 R2를 출력합니다
print(f"MAE : {mean_absolute_error(y1_test, pred_one):.1f}건")   # 기온만 쓴 모델의 MAE를 출력합니다

# ── 18. 비교용: 랜덤포레스트 (같은 70:30 분할) ──
from sklearn.ensemble import RandomForestRegressor   # 나무 여러 그루의 예측을 평균내는 랜덤포레스트 모델을 불러옵니다
rf = RandomForestRegressor(random_state=42, n_jobs=-1)   # 랜덤포레스트를 준비합니다 (random_state로 결과 고정, n_jobs=-1은 CPU 전부 사용)
rf.fit(X_train, y_train)                       # 선형회귀와 똑같은 학습용 데이터로 훈련시킵니다
pred_rf = rf.predict(X_test)                   # 같은 시험용 데이터를 예측합니다
print("\n[랜덤포레스트 - 전체 특성(이슬점 제외)]")   # 제목을 출력합니다
print(f"R2  : {r2_score(y_test, pred_rf):.3f}")   # 랜덤포레스트의 R2를 출력합니다
print(f"MAE : {mean_absolute_error(y_test, pred_rf):.1f}건")   # 랜덤포레스트의 MAE를 출력합니다

# ── 19. 추가 검증: 학습 때 본 적 없는 날짜 예측하기 ──
# 무작위 분할은 같은 날의 앞뒤 시간이 학습에 들어가 있어 점수가 좋게 나올 수 있습니다.
# 그래서 매달 22일 이후 날짜는 통째로 시험용으로 떼어 두고, 나머지 날짜로만 학습합니다.
test_mask = day_of_month.loc[X.index] > 21     # 각 줄이 매달 22일 이후인지(시험용인지) 표시합니다
print(f"\n[처음 보는 날짜로 시험: 학습 {(~test_mask).sum()}행 / 시험 {test_mask.sum()}행]")   # 학습·시험 줄 수를 출력합니다
for name, m in [('선형회귀', LinearRegression()), ('랜덤포레스트', RandomForestRegressor(random_state=42, n_jobs=-1))]:   # 두 모델을 차례로 시험합니다
    m.fit(X[~test_mask], y[~test_mask])        # 22일 이전 날짜로만 학습합니다
    p = m.predict(X[test_mask])                # 학습에 없던 22일 이후 날짜를 예측합니다
    print(f"{name}: R2 {r2_score(y[test_mask], p):.3f}, MAE {mean_absolute_error(y[test_mask], p):.1f}건")   # 점수를 출력합니다
