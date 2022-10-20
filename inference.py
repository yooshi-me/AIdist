import torch
from torchvision import transforms
from PIL import Image
from .ml_model import Net


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
    classes = ('AI_generate', 'photo')

    net = Net()
    inference_model = torch.load(f"./saved_model/cnn_net_ver1.pth")

    with torch.no_grad():
        outputs = net(pre_image) # chage to cpu
        _, predictions = torch.max(outputs, 1)
    print(outputs) # tensor([[ 0.0314, -0.0942]], device='cuda:0')
    print(classes[predictions.item()])

    return outputs

def main():
    image = Image.open('./static/img/predict_img.png')
    pre_image = processing(image)
    outputs = inferance(pre_image)
    print(outputs)
    

if __name__ == "__main__":
    main()