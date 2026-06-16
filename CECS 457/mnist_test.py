import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
import math

# Define a transform to normalize the data
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.,), (1.,))
])

# Download and load the training data
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# Download and load the test data
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1000, shuffle=False)

# Example: get a batch of training data
images, labels = next(iter(train_loader))
#print("Batch of images shape:", images.shape)
#print("Batch of labels shape:", labels.shape)

nn_size = 128


class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(images.shape[2]*images.shape[3], nn_size)
        self.sigmoid = nn.Sigmoid()
        self.l2 = nn.Linear(nn_size, 10)

    def forward(self, x):
        # output1 = self.l1(x)
        # input2 = self.sigmoid(output1)
        # output2 = self.l2(input2)
        # output2 = self.sigmoid(output2)

        return self.l2(self.sigmoid(self.l1(x)))

    def num_par(self):
        return sum(p.numel() for p in self.parameters())


network = SimpleNN()
images = images.reshape(-1, 784)

optim = torch.optim.Adam(params=network.parameters(), lr=0.001)


# Define loss function
loss = nn.CrossEntropyLoss()


# iterations = 500
# history = []
# for i in range(iterations):
#     images, labels = next(iter(train_loader))
#     images = images.reshape(-1, 784)
#     loss_value = loss(network(images), labels)
#     history.append(loss_value.item())
#     loss_value.backward()
#     optim.step()
#     print(f"iteration {i}, loss: {loss_value.item()}")
#
#
# plt.plot(history)
# plt.show()

print("Beginning training")
epochs = 8
history = []
loss_history = [0.0 for i in range(100)]
for epoch in range(1, epochs + 1):
    for step, (images, labels) in enumerate(train_loader):
        images = images.reshape(-1, 784)
        loss_value = loss(network(images), labels)
        loss_history.pop(0)
        loss_history.append(loss_value.item())
        history.append(loss_value.item())
        optim.zero_grad()
        loss_value.backward()
        optim.step()

    optim = torch.optim.Adam(params=network.parameters(), lr=0.01 / (2**epoch))
    loss_avg = 0

    for entry in loss_history:
        loss_avg += entry
    loss_avg /= len(loss_history)

    print(f'Epoch: {epoch}\nAvg. loss: {loss_avg:.4f}')

plt.title("Loss over training time")
plt.plot(history)
plt.show()

correct = 0
total = 0
incorrect_image = None
correct_class = None
model_probs = []

for step, (test_images, test_labels) in enumerate(test_loader):
    test_images = test_images.reshape(-1, 784)
    results = nn.functional.softmax(network(test_images))
    total += len(results)
    for i in range(len(results)):
        if results[i].argmax().item() == test_labels[i].item():
            correct += 1
        elif incorrect_image is None:
            incorrect_image = test_images[i]
            incorrect_image = incorrect_image.reshape(1, 28, 28)
            incorrect_image = incorrect_image.permute(1, 2, 0)
            correct_class = test_labels[i].item()
            for item in results[i]:
                model_probs.append(item.item())

print(f"Overall accuracy: {((correct/total) * 100):.2f}%")
print(f'Correct class: {correct_class}')
highest = 0
predicted = None
for i in range(len(model_probs)):
    print(f'Prob of {i}: {model_probs[i]}')
    if model_probs[i] > highest:
        highest = model_probs[i]
        predicted = i

print(f"Model predicted class {predicted}")
plt.title('Misclassified image')
plt.imshow(incorrect_image, cmap='grey')
plt.show()

