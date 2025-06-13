import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

class Ml_RF:
    # 데이터 불러오기
    df = pd.read_csv("mlb최종.csv", encoding="cp949")

    # 타겟 생성: 은퇴 나이
    df['retire_age'] = df['retire_year'] - df['birth_year']
    df_clean = df.dropna()

    # 사용할 feature 컬럼 정의
    feature_cols = ['G', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'RBI', 'R', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS']
    X = df_clean[feature_cols]
    y = df_clean['retire_age']

    # 정규화 및 분할
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 모델 학습
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 예측
    predictions = model.predict(X_val)

    # 평가 출력
    mse = mean_squared_error(y_val, predictions)
    mae = mean_absolute_error(y_val, predictions)
    r2 = r2_score(y_val, predictions)

    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"R^2: {r2:.4f}")

    # 결과 저장
    df_result = pd.DataFrame({
        "actual_retire_age": y_val.values,
        "predicted_retire_age": predictions
    })
    df_result.to_excel("MLB_RF_예측결과.xlsx", index=False)

    # 시각화
    plt.figure(figsize=(8, 6))
    plt.scatter(y_val, predictions, alpha=0.7)
    plt.plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--')
    plt.xlabel("실제 은퇴 나이")
    plt.ylabel("예측 은퇴 나이")
    plt.title("Random Forest - 은퇴 나이 예측")
    plt.grid(True)
    plt.savefig("MLB_RF_retire_age_scatter.png")
    plt.show()
