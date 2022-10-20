import torch
import torchvision
import torch.nn as nn 
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
from model import Net

def processing(path):
    """"画像の前処理"""
    image_rgba = Image.open(path) # './static/img/predict_img.png'
    image = image_rgba.convert("RGB")
    transform = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Resize(178)]
        )
    image_32 = transform(image)
    image_batch = torch.unsqueeze(image_32, 0)
    return image_batch

def inferance(pre_image):
    """"画像を読み込んで推論する"""
    classes = ('photo', 'AI_generate')
    net = Net()
    net = torch.load('./saved_model/model.pth', map_location=torch.device('cpu')) ###
    with torch.no_grad():
        output = net(pre_image) # chage to cpu
        output = torch.flatten(output)
        prediction = torch.where(output<0.5,0,1)
    print('------------------------------------------------')
    # softmax = nn.Softmax(dim=1)
    # outputs = softmax(outputs)
    label = classes[prediction.item()]
    return output, label

def output_result(path):
    """"前処理と推論の実行 """
    # print('------------------------------------------------')
    # print(image.format, image.size, image.mode)
    # print(image)
    # print(type(image))
    # print('------------------------------------------------')
    pre_image = processing(path)
    output, label = inferance(pre_image)
    return output 
    
if __name__ == "__main__":
    outputs = output_result('./static/img/predict_img.png')
    print(outputs)