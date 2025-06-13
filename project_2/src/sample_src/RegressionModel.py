################################################################################
#
#   Sample
#   머신러닝
#   RegressionModel
#   튜닝 필요  
#    
################################################################################

from torch import nn
    # 모델 정의
class RegressionModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.net(x)