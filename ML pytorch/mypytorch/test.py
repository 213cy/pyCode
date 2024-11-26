import torch
import torch.nn as nn
from torch.utils.data import TensorDataset,DataLoader
# import numpy as np

N = 5

# myseed = 42069  # set a random seed for reproducibility
# # np.random.seed(myseed)
# torch.manual_seed(myseed)

# Create data loaders.
d = torch.randint(0, 199, (20000,N), dtype = torch.float )
l = d.argmax( dim = 1 )
training_data = dataset = TensorDataset(d, l)
batch_size = 64
train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)


# Define model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(N, 2* N),
            nn.ReLU(),
            nn.Linear(2*N, 2*N),
            nn.ReLU(),
            nn.Linear(2 * N, N)
        )

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


model = Net()
# print(model)
# print("Model's state_dict:")
# for param_tensor in model.state_dict():
#     print(param_tensor, "\t", model.state_dict()[param_tensor])

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

def train(dataloader, model, loss_fn, optimizer):
    data_size = len(dataloader.dataset)
    batch_size = dataloader.batch_size
    model.train()
    # for k in range(size):
    #     X = torch.randint(0, 555, (7,), dtype = torch.float32 )
    #     y = X.argmax()
    #     # print(torch.where(X==X.max())[0].size())
        # # a = loss_fn(torch.tensor([1,2,3,4],dtype = torch.float),torch.tensor(2))
        # # print(a)
        # loss = loss_fn(pred.unsqueeze(0), y.unsqueeze(0))

    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction error
        pred = model(X)
        # yy = torch.zeros_like(pred).scatter_(dim=1, index=y.unsqueeze(1),value=1)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # batch = k
        if batch % 20 == 0:
            # print(X.tolist(),pred.argmax(0).item(),y.item())
            correct =  (pred.argmax(1) == y).sum().item()
            loss = loss.item()
            current = (batch + 1) * batch_size
            print(f"correct: {correct:>3d}/{batch_size}  " 
            f"loss: {loss:>7f}  [{current:>5d}/{data_size}]")

epochs = 20
for t in range(epochs):
    print(f"      Epoch {t+1}")
    train(train_dataloader, model, loss_fn, optimizer)
    print("--------------------------------------")

print("Done!")






