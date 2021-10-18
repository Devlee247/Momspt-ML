import torch.nn as nn

# Gesture Inference From Video
class GIFV(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(14,4)
    def forward(self, x):
        return self.linear(x)