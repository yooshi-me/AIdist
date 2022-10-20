import torch
import torch.nn as nn
from dataset import get_loader,CustomImageDataset
import matplotlib.pyplot as plt
from model import Net
import os
import datetime


def main():
    batch_size = 1
    paths_list_path = "./data/pahts_list_inference.csv"
    model_path = "./out/2022-10-17-04-25-07/model_weight.pth"
    out_path = "./out"

    # 出力用ディレクトリ準備
    out_path = os.path.join(out_path,datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"_inference")

    #google_drive_accese()

    data_for_glaph = {"train":[],"test":[]}

    # データローダー取得
    _,testloader = get_loader(paths_list_path,batch_size,inference_flag=True)



    # モデル準備   
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device is",device)
    net = torch.load(model_path)
    net = net.to(device)
    loss_fn = nn.BCELoss()

    ims = []
    
    #学習、テスト
    try:
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
                img = inputs[0].to('cpu').detach().numpy().transpose(1, 2, 0)
                ims.append([img,int(labels[0].item()),predicted[0].item(),outputs[0].item()])
                correct += (predicted==labels).sum().item()
            all_loss /= len(testloader)
            correct /= test_size
            correct *= 100
            print(f"Accuracy: {correct:>5f}% loss:{all_loss:>5f}")

    except KeyboardInterrupt:
        pass

    os.mkdir(out_path)

    cnt = 0
    for fig_count in range(int(len(ims)/9)):
        fig,axs = plt.subplots(3,3)
        fig.suptitle("label,pred,outputs")
        ar = axs.ravel()
        for i in range(9):
            ar[i].axis('off')
            ar[i].set_title(str(ims[cnt][1])+","+str(ims[cnt][2])+","+str(format(ims[cnt][3],".2f")))
            ar[i].imshow(ims[cnt][0])
            cnt += 1
        fig.savefig(os.path.join(out_path,"fig_"+str(fig_count)+".png"))

if __name__ == "__main__":
    main()