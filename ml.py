import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from dataset import get_loader,CustomImageDataset
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



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
        self.fc1 = nn.Linear(4*4*256,4096)
        self.fc2 = nn.Linear(4096,10)
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
        x = x.view(-1,4*4*256)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x


def google_drive_accese():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

def main():
    epochs = 50
    lr = 1e-3

    paths_list_path = "./data/pahts_list.csv"

    google_drive_accese()
    trainloader,testloader = get_loader(paths_list_path)
    

    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    net = Net()
    net = net.to(device)

    optimizer = optim.Adam(net.parameters(),lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    

    for epoch in range(epochs):
        running_loss = 0
        print(f"epoch:{epoch+1:>d} ------------------------")
        for i, (inputs,labels) in enumerate(trainloader):
            correct = 0
            optimizer.zero_grad()
            inputs,labels = inputs.to(device),labels.to(device)

            outputs = net(inputs)
            loss = loss_fn(outputs,labels)

            running_loss += loss.item()
            correct += (outputs.argmax(1) == labels).sum().item()
            loss.backward()
            optimizer.step()
        
        all_loss = loss.item()
        correct /= inputs.size(0)
        correct *= 100
        
        print(f"Accuracy: {correct:>5f}% loss:{all_loss:>5f}")  
        """






    


if __name__ == "__main__":
    main()