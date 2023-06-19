"""SHARE MLSpring2021 - HW2-1.ipynb
# **Homework 2-1 Phoneme Classification**

## Data
- `train_11.npy`: training data<br>
- `train_label_11.npy`: training label<br>
- `test_11.npy`:  testing data<br><br>
"""
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader


"""## Preparing Data"""
print('Loading data ...')
train = np.load('./train_11.npy')
train_label = np.load('./train_label_11.npy')
##breakpoint()
# test = np.load('test_11.npy')
print('Size of original training data: {}'.format(train.shape))
##aa = np.kron( np.array([0.8, 0.85, 0.9, 1, 1.1, 1.3, 1.1, 1, 0.9, 0.85, 0.8]),np.ones(39))
##train *= aa
##train[:,0]=np.arange(train.shape[0])
print('Size of marked training data: {}'.format(train.shape))


"""## Create Dataset"""
class TIMITDataset(Dataset):
    Cof = np.kron( np.array([0.8, 0.85, 0.9, 1, 1.1, 1.3, 1.1, 1, 0.9, 0.85, 0.8]),np.ones(39))
    def __init__(self, X, y=None):
        self.data = torch.from_numpy(X).float()
##        self.data = torch.from_numpy(TIMITDataset.Cof*X).float()
        self.length = len(self.data)
        if y is not None:
            y = y.astype( int )
            self.label = torch.LongTensor(y)
        else:
            self.label = None

    def __getitem__(self, idx):
        if self.label is not None:
            return self.data[idx], self.label[idx]
        else:
            return self.data[idx]

    def __len__(self):
##        print( len(self.data) == self.length)
        return self.length



"""Create a data loader from the dataset."""
print('Create a data loader from the dataset ...')
BATCH_SIZE = 64
print('Create dataset ...')
train_set = TIMITDataset(train, train_label)
##print('Create data loader ...')
##train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
##test = val_x


"""Cleanup the unneeded variables to save memory."""
import gc
del train, train_label
gc.collect()


"""## Create Model"""
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        self.layer1 = nn.Linear(429, 1024)
        self.layer2 = nn.Linear(1024, 512)
        self.layer3 = nn.Linear(512, 128)
        self.out = nn.Linear(128, 39)

        self.act_fn = nn.Sigmoid()

    def forward(self, x):
        x = self.layer1(x)
        x = self.act_fn(x)

        x = self.layer2(x)
        x = self.act_fn(x)

        x = self.layer3(x)
        x = self.act_fn(x)

        x = self.out(x)

        return x

"""## Training"""
#check device
def get_device():
  return 'cuda' if torch.cuda.is_available() else 'cpu'


# get device
device = get_device()
print(f'DEVICE: {device}')

# training parameters
num_epoch = 0               # number of training epoch
learning_rate = 0.001       # learning rate

# the path where checkpoint saved
model_path = './model.ckpt'

# create model, define a loss function, and optimizer
model = Classifier().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# start training

best_rate = 0.0
c_rate=0.0
train_acc = 0.0
l_mean=3.0
for epoch in range(num_epoch):

    train_loss = 0.0

    # training
    model.train() # set the model to training mode

##    breakpoint()
    b_size=np.random.randint( 30,30+20*l_mean )
    print('set batch size to {}'.format( b_size ))
    train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
    
##    print( train_loader.batch_size )
    for i, data in enumerate(train_loader):

        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        batch_loss = criterion(outputs, labels)
        _, train_pred = torch.max(outputs, 1) # get the index of the class with the highest probability

        c_count = (train_pred.cpu() == labels.cpu()).sum().item()
        c_rate = (   ( 2000-inputs.size(0) )*c_rate + c_count   ) / 2000
        # if the model improves, save a checkpoint at this epoch
        if c_rate > best_rate and c_rate > 0.7:
            best_rate = c_rate
            torch.save(model.state_dict(), model_path)
            print('saving model with correct rate {:.3f}'.format( best_rate ))
        
        batch_loss.backward()
        optimizer.step()

        train_loss += batch_loss.item()

    l_mean = train_loss/len(train_loader) 
    print('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f}'.format(
        epoch + 1, num_epoch, c_rate,    l_mean ))
##    print('count={}'.format(c_count))
            
print('saved model until last epoch with acc {:.3f}'.format(best_rate)  )


##raise SystemExit

"""## Testing"""
# create testing dataset
test_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=False)
# create model and load weights from checkpoint
model_path = './model21.ckpt'
model = Classifier().to(device)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu') ))


"""Make prediction."""
predict = []
c_count = 0
model.eval() # set the model to evaluation mode
with torch.no_grad():
    for i, data in enumerate(test_loader):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, test_pred = torch.max(outputs, 1) # get the index of the class with the highest probability

        c_count += (test_pred.cpu() == labels.cpu()).sum().item()
        
print('{} / {} = {}'.format(c_count, len(train_set), c_count/len(train_set)) )


