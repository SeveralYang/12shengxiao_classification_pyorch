import torch
from torch import nn
from torch.optim import SGD
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms

from dataset import MyDataSet
from model import build_model

if __name__ == '__main__':
    writer = SummaryWriter("../weight")
    train_set = MyDataSet(
        txt_path="../train.txt",
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize([256, 256]),
            transforms.RandomHorizontalFlip(),
            transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5])
        ])
    )

    test_set = MyDataSet(
        txt_path="../test.txt",
        transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize([256, 256]),
            transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5])
        ])
    )

    train_size = len(train_set)
    test_size = len(test_set)
    train_loader = DataLoader(dataset=train_set, batch_size=16, shuffle=True)
    test_loader = DataLoader(dataset=test_set, batch_size=16, shuffle=True)

    # 神经网络模型
    model = build_model(12)
    model.cuda()
    # 损失函数
    loss_function = nn.CrossEntropyLoss()
    loss_function = loss_function.cuda()  # 使用GPU计算
    # 优化器 （模型结构，学习速率）
    learn_rate = 0.01
    optimizer = SGD(model.parameters(), lr=learn_rate)

    total_train = 0  # 记录训练次数
    epoch = 100  # 计划训练轮次

    for i in range(epoch):  # i 记录测试次数
        if i == 10:
            learn_rate = 0.05
            optimizer = SGD(model.parameters(), lr=learn_rate)
        if i == 20:
            learn_rate = 0.001
            optimizer = SGD(model.parameters(), lr=learn_rate)

        print('---开始第{}轮训练---'.format(i + 1))
        for img, target in train_loader:
            img = img.cuda()  # 使用GPU计算
            target = target.cuda()  # 使用GPU计算
            output = model(img)
            loss = loss_function(output, target)  # 实际输出和训练目标之间的距离
            optimizer.zero_grad()  # 优化器参数归零
            loss.backward()  # 误差反馈
            optimizer.step()  # 优化器根据反馈 优化模型
            total_train += 1

            print('训练次数{}，当前误差{}'.format(total_train + 1, loss.item()))
            writer.add_scalar('训练集损失', loss.item(), total_train)

        print('---第{}轮训练完成，开始测试---'.format(i + 1))
        total_loss = 0
        correct = 0
        # 测试 不进行梯度调优
        with torch.no_grad():
            for img, target in test_loader:
                img = img.cuda()  # 使用GPU计算
                target = target.cuda()  # 使用GPU计算
                output = model(img)
                loss = loss_function(output, target)
                total_loss += loss.item()
                correct += (output.argmax(1) == target).sum()
        print('---第{}轮测试完成，本轮总误差{},正确率{}---'.format(i + 1, total_loss, correct / test_size))
        writer.add_scalar('测试集正确率', correct / test_size, i)
        # 保存训练模型
        torch.save(model.state_dict(), f'../weight/{i}epoch_correct{correct / test_size}.pth')
    writer.close()
