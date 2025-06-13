
################################################################################
#
#   Sample
#   머신러닝
#   LinearRegression  
#    
################################################################################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

class ML_LR:
    # 데이터 불러오기
    df = pd.read_excel("생년_결측치_예측값포함 (1).xlsx")

    # 파생 변수 생성
    df['retire_age'] = df['last_year'] - df['estimated_birth_year']
    df_clean = df.dropna()

    # 특성과 타겟 정의
    feature_cols = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'SLG', 'AVG', 'active_year']
    X = df_clean[feature_cols]
    y = df_clean['retire_age']

    # 정규화 및 분할
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 선형 회귀 모델 학습
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 예측
    predictions = model.predict(X_val)

    # 평가
    mse = mean_squared_error(y_val, predictions)
    mae = mean_absolute_error(y_val, predictions)
    r2 = r2_score(y_val, predictions)

    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"R^2: {r2:.4f}")

# # 결과 저장
# df_result = pd.DataFrame({
#     "actual_retire_age": y_val.values,
#     "predicted_retire_age": predictions
# })
# df_result.to_excel("LR_예측결과_retire_age.xlsx", index=False)

# # 시각화
# plt.figure(figsize=(8, 6))
# plt.scatter(y_val, predictions, alpha=0.7)
# plt.plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--')
# plt.xlabel("Actual Retire Age")
# plt.ylabel("Predicted Retire Age")
# plt.title("Retire Age Prediction (Linear Regression)")
# plt.grid(True)
# plt.savefig("LR_retire_age_scatter.png")
# plt.show()
