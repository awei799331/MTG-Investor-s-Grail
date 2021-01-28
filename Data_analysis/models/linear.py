import torch
import torch.nn as nn
import torchvision.models as models

class PureLinear(nn.Module):

    def __init__(self, num_features):
        super(PureLinear, self).__init__()

        self.linear1 = nn.Linear(num_features, 50)
        self.prelu = nn.PReLU()
        self.linear2 = nn.Linear(50, 30)

    def forward(self, x):

        x = self.linear1(x)
        x = self.prelu(x)
        x = self.linear2(x)

        return x