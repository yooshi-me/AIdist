import torch
import torchvision
import torch.nn as nn 
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
# from ml_model import Net


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = self.pool(F.relu(self.conv1(x)))
        # If the size is a square, you can specify with a single number
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

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
    net.load_state_dict(torch.load("./saved_model/cnn_structure_ver1.pth", map_location=torch.device('cpu')))
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
    output_result('./static/img/predict_img.png')