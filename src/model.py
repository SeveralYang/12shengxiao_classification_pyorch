from torch import nn
from torchvision import models


def build_model(num_classes):
    transfer_model = models.resnet18(pretrained=True)
    for param in transfer_model.parameters():
        param.requires_grad = False

    # 修改最后一层维数，即 把原来的全连接层 替换成 输出维数为2的全连接层
    dim = transfer_model.fc.in_features
    transfer_model.fc = nn.Linear(dim, num_classes)

    return transfer_model
