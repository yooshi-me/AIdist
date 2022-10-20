import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from dataset import get_loader,CustomImageDataset
from model import Net
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
import cv2




def make_figure():
    acc_fig = plt.figure(figsize=(12,8))
    plt.rcParams["font.size"] = 25
    acc_ax = acc_fig.add_subplot(111,xlabel="Epoch",ylabel="Accuracy")
    acc_ax.set_ylim(0,100)

    loss_fig = plt.figure(figsize=(12,8))
    plt.rcParams["font.size"] = 25
    loss_ax = loss_fig.add_subplot(111,xlabel="Epoch",ylabel="Loss")

    return acc_fig,loss_fig,acc_ax,loss_ax

def check_inputs_data(inputs,labels):
    for input,label in zip(inputs,labels):
        img = input.to('cpu').detach().numpy().transpose(1, 2, 0)
        plt.axis('off')
        if label.item()==0:
            label="generated"
        else:
            label="cifar-10"
        plt.title(label)
        plt.imshow(img)
        plt.show()

def train_loop(trainloader,optimizer,loss_fn,net,device,data_for_glaph):
    running_loss = 0
    all_loss = 0
    train_size = len(trainloader.dataset)
    for i, (inputs,labels) in enumerate(trainloader):
        correct = 0
        optimizer.zero_grad()
        #check_inputs_data(inputs,labels)
        inputs,labels = inputs.to(device),labels.to(device)

        outputs = net(inputs)
        outputs = torch.flatten(outputs)
        labels = labels.to(torch.float32)
        loss = loss_fn(outputs,labels)

        running_loss += loss.item()
        all_loss += loss.item()
        predicted = torch.where(outputs<0.5,0,1)
        correct += (predicted==labels).sum().item()
        loss.backward()
        optimizer.step()

        if i % 100 == 99: 
            running_loss /= 100
            print(f"loss:{running_loss:>5f} [{i*len(inputs)}]/[{train_size}]")
            running_loss = 0
    
    all_loss /= len(trainloader)
    correct /= inputs.size(0)
    correct *= 100
    
    data_for_glaph["train"].append([correct,all_loss])
    print(f"Train Accuracy: {correct:>5f}% loss:{all_loss:>5f}")

    return data_for_glaph

def test_loop(testloader,loss_fn,net,device,data_for_glaph):
    test_size = len(testloader.dataset)
    all_loss = 0
    correct = 0
    with torch.no_grad():
        for inputs,labels in testloader:
            inputs,labels = inputs.to(device),labels.to(device)

            outputs = net(inputs)
            outputs = torch.flatten(outputs)
            labels = labels.to(torch.float32)
            loss = loss_fn(outputs,labels)
            all_loss += loss.item()
            predicted = torch.where(outputs<0.5,0,1)
            correct += (predicted==labels).sum().item()
        all_loss /= len(testloader)
        correct /= test_size
        correct *= 100
        data_for_glaph["test"].append([correct,all_loss])
        print(f"Test Accuracy: {correct:>5f}% loss:{all_loss:>5f}")
    
    return data_for_glaph

def google_drive_accese():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

def main():
    # ハイパーパラメータ
    epochs = 10
    batch_size = 10
    lr = 1e-3
    paths_list_path = "./data/pahts_list_without_black_img.csv"
    out_path = "./out"

    # 出力用ディレクトリ準備
    out_path = os.path.join(out_path,datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    #google_drive_accese()

    # データローダー取得
    trainloader,testloader = get_loader(paths_list_path,batch_size)

    # グラフ準備
    acc_fig, loss_fig, acc_ax, loss_ax = make_figure()


    # モデル準備   
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device is",device)
    net = Net()
    net = net.to(device)

    optimizer = optim.Adam(net.parameters(),lr=lr)
    loss_fn = nn.BCELoss()
    data_for_glaph = {"train":[],"test":[]}
    
    #学習、テスト
    try:
        for epoch in range(epochs):
            print(f"epoch:{epoch+1:>d} ------------------------")
            data_for_glaph = train_loop(trainloader,optimizer,loss_fn,net,device,data_for_glaph)
            data_for_glaph = test_loop(testloader,loss_fn,net,device,data_for_glaph)

    except KeyboardInterrupt:
        pass
    
    # グラフプロット
    if len(data_for_glaph["test"]) > 1:
        for mode in ["train","test"]:
            data_for_glaph[mode] = np.array(data_for_glaph[mode])
            acc_ax.plot(range(len(data_for_glaph[mode])),data_for_glaph[mode][:,0],label=mode)
            loss_ax.plot(range(len(data_for_glaph[mode])),data_for_glaph[mode][:,1],label=mode)
    
    # 結果出力、保存
    os.mkdir(out_path)
    torch.save(net, os.path.join(out_path, 'model.pth'))
    torch.save(net.state_dict(), os.path.join(out_path, 'weight.pth'))
    acc_fig.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0)
    acc_fig.savefig(os.path.join(out_path,"accuracy_figure"))
    loss_fig.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0)    
    loss_fig.savefig(os.path.join(out_path,"loss_figure"))


if __name__ == "__main__":
    main()