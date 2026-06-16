import torch
import torch.nn as nn
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# Define a transform to normalize the data
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.,), (1.,))
])

# Download and load the training data
train_dataset = datasets.cifar.CIFAR10(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# Download and load the test data
test_dataset = datasets.cifar.CIFAR10(root='./data', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1000, shuffle=False)


images, labels = next(iter(train_loader))
print("Batch of images shape:", images.shape)
# print("Batch of labels shape:", labels.shape)


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5)
        self.max_pool1 = nn.MaxPool2d(kernel_size=3)
        self.max_pool2 = nn.MaxPool2d(kernel_size=2)
        self.fc1 = nn.Linear(256, 200)
        self.fc2 = nn.Linear(200, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        # conv1 -> max_pool1 -> relu-> conv2 -> max_pool2 -> relu -> view(-1, 256) -> fc1 -> relu -> fc2
        return self.fc2(
            self.relu(
                self.fc1(
                    self.relu(
                        self.max_pool2(
                            self.conv2(
                                self.relu(
                                    self.max_pool1(
                                        self.conv1(x)
                                    )
                                )
                            )
                        )
                    ).view(-1, 256)
                )
            )
        )
        # x = self.conv1(x)
        # x = self.max_pool1(x)
        # x = self.relu(x)
        # x = self.conv2(x)
        # x = self.max_pool2(x)
        # x = self.relu(x)
        # x = x.view(-1, 256)
        # x = self.fc1(x)
        # x = self.relu(x)
        # x = self.fc2(x)
        # return x


ConvNN = Net()

print(f'Final output shape: {ConvNN(images).shape}')

loss_history = [0.0 for i in range(100)]
epochs = 8
criterion = nn.CrossEntropyLoss()
history = []


for epoch in range(1, epochs + 1):
    optim = torch.optim.Adam(params=ConvNN.parameters(), lr=0.001)
    for step, (images, labels) in enumerate(train_loader):
        loss_value = criterion(ConvNN(images), labels)
        loss_history.pop(0)
        loss_history.append(loss_value.item())
        history.append(loss_value.item())
        optim.zero_grad()
        loss_value.backward()
        optim.step()

    loss_avg = 0

    for entry in loss_history:
        loss_avg += entry
    loss_avg /= len(loss_history)

    print(f'Epoch: {epoch}\nAvg. loss: {loss_avg:.4f}')


plt.title("Loss over training time")
plt.plot(history)
plt.show()
