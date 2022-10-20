import pandas as pd
import torch
import os
import pandas as pd
from torchvision import transforms
from torchvision.io import read_image
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import PIL

def get_loader(paths_list_path,batch_size,test_size=0.2,inference_flag=False):
    paths_dataframe = pd.read_csv(paths_list_path)

    transform = transforms.Compose(
        [transforms.ToTensor(), # ToTensorによる変換でfloatになる
         transforms.Resize(178)]
    )

    if inference_flag:
        testdataset=CustomImageDataset(img_labels=paths_dataframe["generated_flag"].to_list(), img_dir=paths_dataframe["path"].to_list(),transform=transform,target_transform=None)
        testloader = torch.utils.data.DataLoader(testdataset, batch_size=batch_size, shuffle=False)
        return None, testloader



    train_dir, test_dir, train_label, test_label = train_test_split(paths_dataframe["path"].to_list(),paths_dataframe["generated_flag"].to_list(),test_size=test_size,random_state=42,shuffle=True, stratify=paths_dataframe["generated_flag"].to_list())

    

    traindataset = CustomImageDataset(img_labels=train_label, img_dir=train_dir,transform=transform,target_transform=None)
    testdataset = CustomImageDataset(img_labels=test_label, img_dir=test_dir,transform=transform,target_transform=None)
    

    trainloader = torch.utils.data.DataLoader(traindataset, batch_size=batch_size, shuffle=True)
    testloader = torch.utils.data.DataLoader(testdataset, batch_size=batch_size, shuffle=False)

    

    return trainloader,testloader

class CustomImageDataset(Dataset):
    def __init__(self, img_labels, img_dir, transform=None, target_transform=None):
        self.img_labels = img_labels
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        image = PIL.Image.open(self.img_dir[idx]) # PILで画像を開く(ToTensorのために必要)
        label = self.img_labels[idx]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label

