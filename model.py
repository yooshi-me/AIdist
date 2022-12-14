import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(3,64,5,padding=2)
        self.conv2 = nn.Conv2d(64,64,5,padding=2)
        self.pool = nn.MaxPool2d(2,2)
        self.conv3 = nn.Conv2d(64,128,3,padding=1)
        self.conv4 = nn.Conv2d(128,128,3,padding=1)
        self.conv5 = nn.Conv2d(128,256,3,padding=1)
        self.conv6 = nn.Conv2d(256,256,3,padding=1)
        self.conv7 = nn.Conv2d(256,512,3,padding=1)
        self.conv8 = nn.Conv2d(512,512,3,padding=1)
        self.conv9 = nn.Conv2d(512,1024,3,padding=1)
        self.conv10 = nn.Conv2d(1024,1024,3,padding=1)
        self.fc1 = nn.Linear(5*5*1024,4096)
        self.fc2 = nn.Linear(4096,1)
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.25)
    
    def forward(self,x):
        x = F.relu(self.conv1(x))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.dropout(x)
        x = F.relu(self.conv3(x))
        x = self.pool(F.relu(self.conv4(x)))
        x = self.dropout(x)
        x = F.relu(self.conv5(x))
        x = self.pool(F.relu(self.conv6(x)))
        x = self.dropout(x)
        x = F.relu(self.conv7(x))
        x = self.pool(F.relu(self.conv8(x)))
        x = self.dropout(x)
        x = F.relu(self.conv9(x))
        x = self.pool(F.relu(self.conv10(x)))
        x = self.dropout(x)
        x = x.view(-1,5*5*1024)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.sigmoid(x)

        return x