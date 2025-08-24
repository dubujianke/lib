import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import confusion_matrix

import torch
from torch.utils.data import Dataset, DataLoader
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("使用设备:", device)
class SampleDataset(Dataset):
    def __init__(self, filename):
        self.data = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                label_str, sample_str = line.split("#")
                label = float(label_str)

                # 逗号分隔 -> 第一维
                vectors = []
                for vec in sample_str.split(","):
                    numbers = [float(x) for x in vec.strip().split()]
                    vectors.append(numbers)

                # 转为 Tensor (1, H, W)，CNN 输入需要通道维度
                tensor = torch.tensor(vectors, dtype=torch.float32).unsqueeze(0)
                self.data.append((tensor, torch.tensor(label, dtype=torch.long)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, input_shape, num_classes=2):
        super(SimpleCNN, self).__init__()
        C, H, W = input_shape  # 输入通道，高，宽

        self.conv1 = nn.Conv2d(C, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.pool2 = nn.MaxPool2d(2, 2)
        def conv_out_size(size):
            return size // 4  # 两次池化后缩小4倍

        H_out, W_out = conv_out_size(H), conv_out_size(W)

        self.fc1 = nn.Linear(32 * H_out * W_out, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.5)
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


import torch.optim as optim
import os


# 数据集 & DataLoader
dataset = SampleDataset(r"d:/stock/data/ret_2025_08_08.txt")
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
# 取一个样本推断输入尺寸
sample_x, _ = dataset[0]
model = SimpleCNN(sample_x.shape).to(device)

# 损失函数加权
class_weights = torch.tensor([1.0, 100.0], dtype=torch.float32).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.Adam(model.parameters(), lr=0.001)

model_path = "cnn_model_weights.pth"
if os.path.exists(model_path):
    print("发现已保存模型，加载中...")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.train()  # 切换回训练模式
    print("模型已加载，继续训练。")
else:
    print("未发现模型，从头训练。")

save_interval = 100
# 训练
for epoch in range(0):  # 10个epoch
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.long().to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch + 1}, Loss: {running_loss / len(dataloader):.4f}")

    if (epoch + 1) % save_interval == 0:
        torch.save(model.state_dict(), model_path)
        print(f"已保存模型，轮次: {epoch+1}")



model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    model.eval()
    for inputs, labels in dataloader:  # 或 val_loader
        inputs = inputs.to(device)
        labels = labels.long().to(device)
        outputs = model(inputs)
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        break

cm = confusion_matrix(all_labels, all_preds)
print("混淆矩阵:\n", cm)
# 二分类
TP = cm[1, 1]
FN = cm[1, 0]
TPR = TP / (TP + FN) if (TP + FN) > 0 else 0.0
print(f"真正率 (TPR / Recall): {TPR:.4f}")

with torch.no_grad():
    model.eval()
    for inputs, labels in dataloader:  # 或 val_loader
        inputs = inputs.to(device)
        labels = labels.long().to(device)
        outputs = model(inputs)
        preds = torch.argmax(outputs, dim=1)
        print(preds.numpy(), labels)


