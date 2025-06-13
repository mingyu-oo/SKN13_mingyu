################################################################################
#
#   Sample
#   딥러닝
#   RegressionModel
#   
################################################################################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
from RegressionModel import RegressionModel as rg
from train import Train
from util import Utils

class Deep:
    # 데이터 불러오기
    df = pd.read_excel("생년_결측치_예측값포함 (1).xlsx")
    df['retire_age'] = df['last_year'] - df['estimated_birth_year']
    df_clean = df.dropna()

    # 특성 및 타겟 지정
    feature_cols = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'SLG', 'AVG', 'active_year']
    X = df_clean[feature_cols]
    y = df_clean['retire_age']

    # 정규화 및 분할
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 텐서 변환
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    y_val_tensor = torch.tensor(y_val.values, dtype=torch.float32).unsqueeze(1)

    train_ds = TensorDataset(X_train_tensor, y_train_tensor)
    val_ds = TensorDataset(X_val_tensor, y_val_tensor)
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)

    # 회귀 모델 정의
    class RegressionModel(rg.nn.Module):
        def __init__(self, input_dim):
            super().__init__()
            self.net = rg.nn.Sequential(
                rg.nn.Linear(input_dim, 64),
                rg.nn.ReLU(),
                rg.nn.Linear(64, 1)
            )
        def forward(self, x):
            return self.net(x)

    # 모델 학습
    model = RegressionModel(len(feature_cols))
    loss_fn = rg.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    train_loss_list, train_accuracy_list, val_loss_list, val_accuracy_list = Train.fit(
        train_loader, val_loader, model, loss_fn, optimizer,
        epochs=100, save_best_model=False, device='cpu', mode='multi'
    )

    # # 예측 결과 저장
    # model.eval()
    # with torch.no_grad():
    #     predictions = model(X_val_tensor).squeeze().numpy()

    # df_result = pd.DataFrame({
    #     "actual_retire_age": y_val.values,
    #     "predicted_retire_age": predictions
    # })
    # df_result.to_excel("DL_예측결과_retire_age.xlsx", index=False)

    # # 시각화
    # Utils.plot_fit_result(train_loss_list, train_accuracy_list, val_loss_list, val_accuracy_list)
