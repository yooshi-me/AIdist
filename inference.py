import torch
import torchvision
import torch.nn as nn 
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
from ml_model import Net

def processing(image):
    """"画像の前処理"""
    transform = transforms.Compose(
            [transforms.ToTensor(),
            transforms.Resize(32)]
        )
    image_32 = transform(image)
    image_batch = torch.unsqueeze(image_32, 0)
    return image_batch

def inferance(pre_image):
    """"画像を読み込んで推論する"""
    classes = ('AI_generate', 'photo')
    print('ここまでok1')
    net = Net()
    print('ここまでok2')
    net = torch.load('./saved_model/cnn_structure_ver1.pth', map_location=torch.device('cpu')) ###
    print('ここまでok3')
    with torch.no_grad():
        outputs = net(pre_image) # chage to cpu
        _, predictions = torch.max(outputs, 1)

    softmax = nn.Softmax(dim=1)
    outputs = softmax(outputs)
    label = classes[predictions.item()]
    print('ここまでok4')
    return outputs, label

def output_result(path):
    image_rgba = Image.open(path) # './static/img/predict_img.png'
    
    image = image_rgba.convert("RGB")

    # print('------------------------------------------------')
    # print(image.format, image.size, image.mode)
    # print(image)
    # print(type(image))
    # print('------------------------------------------------')
    pre_image = processing(image)
    outputs, label = inferance(pre_image)
    return outputs    
    
if __name__ == "__main__":
    outputs = output_result('./static/img/predict_img.png')
    print(outputs)