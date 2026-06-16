import torch
import torch.nn as nn
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

target = 3

# Define a transform to normalize the data
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.,), (1.,))
])


# Download and load the training data
train_dataset = datasets.cifar.CIFAR10(root='./data', train=True, download=True, transform=transform)
filtered_indices = [i for i, y in enumerate(train_dataset.targets) if y == target]
train_dataset = torch.utils.data.Subset(train_dataset, filtered_indices)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# Download and load the test data
test_dataset = datasets.cifar.CIFAR10(root='./data', train=False, download=True, transform=transform)
filtered_indices = [i for i, y in enumerate(test_dataset.targets) if y == target]
test_dataset = torch.utils.data.Subset(test_dataset, filtered_indices)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1000, shuffle=False)


images, labels = next(iter(train_loader))
print("Batch of images shape:", images.shape)


def add_noise(dataset, std=0.05):
    noise = torch.randn_like(dataset) * std
    noisy_images = dataset + noise
    noisy_images = torch.clamp(noisy_images, 0.0, 1.0)
    return noisy_images


class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=6)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=7)
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=4, stride=2)
        self.conv4 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=2)
        self.conv5 = nn.Conv2d(in_channels=32, out_channels=8, kernel_size=4)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = self.conv3(x)
        x = nn.functional.relu(x)
        x = self.conv4(x)
        x = nn.functional.relu(x)
        x = self.conv5(x)
        x = nn.functional.relu(x)
        return x


class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.ConvTranspose2d(in_channels=8, out_channels=32, kernel_size=4)
        self.conv2 = nn.ConvTranspose2d(in_channels=32, out_channels=32, kernel_size=4)
        self.conv3 = nn.ConvTranspose2d(in_channels=32, out_channels=32, kernel_size=3, stride=2)
        self.conv4 = nn.ConvTranspose2d(in_channels=32, out_channels=32, kernel_size=3, stride=2)
        self.conv5 = nn.ConvTranspose2d(in_channels=32, out_channels=3, kernel_size=2)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = self.conv3(x)
        x = nn.functional.relu(x)
        x = self.conv4(x)
        x = nn.functional.relu(x)
        x = self.conv5(x)
        x = nn.functional.relu(x)
        return x


class Autoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def forward(self, x):
        return self.decoder(self.encoder(x))


model = Autoencoder()

print('Final output shape:', model(images).shape)

inspection = False
if inspection:
    for inspect in images:
        inspect = inspect.reshape(3, 32, 32)
        inspect = inspect.permute(1, 2, 0)
        fig, axes = plt.subplots(1, 2, figsize=(8, 4))

        axes[0].imshow(inspect)
        axes[1].imshow(add_noise(inspect))
        plt.tight_layout()
        plt.show()


loss_history = [0.0 for i in range(len(filtered_indices))]
epochs = 8
criterion = nn.MSELoss()
history = []


for epoch in range(1, epochs + 1):
    optim = torch.optim.Adam(params=model.parameters(), lr=0.001 / epoch)
    for step, (images, labels) in enumerate(train_loader):
        loss_value = criterion(model(add_noise(images)), images)
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
