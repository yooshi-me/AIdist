import torch
import torchvision
import torch.nn as nn 
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
from model import Net
import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from PIL import ImageFile 
ImageFile.LOAD_TRUNCATED_IMAGES = True

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
    label = classes[prediction.item()]
    return output, label

def output_result(path,gradcam_flag=False):
    """"前処理と推論の実行 """
    pre_image = processing(path)
    if gradcam_flag:
        output, label  = gradcam(path)
    else:
        output, label = inferance(pre_image)
    return output


def gradcam(img_path):
    classes = ('photo', 'AI_generate')
    net = torch.load('./saved_model/model.pth', map_location=torch.device('cpu')) ###
    net.eval()

    def __extract(grad):
        global feature_grad
        feature_grad = grad

    img = processing(img_path)

    # get features from the last convolutional layer
    x = F.relu(net.conv1(img))
    x = net.pool(F.relu(net.conv2(x)))
    x = net.dropout(x)
    x = F.relu(net.conv3(x))
    x = net.pool(F.relu(net.conv4(x)))
    x = net.dropout(x)
    x = F.relu(net.conv5(x))
    x = net.pool(F.relu(net.conv6(x)))
    x = net.dropout(x)
    x = F.relu(net.conv7(x))
    x = net.pool(F.relu(net.conv8(x)))
    x = net.dropout(x)
    x = F.relu(net.conv9(x))
    x = F.relu(net.conv10(x))
    features = x

    # hook for the gradients
    def __extract_grad(grad):
        global feature_grad
        feature_grad = grad
    features.register_hook(__extract_grad)

    # get the output from the whole VGG architecture
    x = net.pool(x)
    x = x.view(-1,5*5*1024)
    x = F.relu(net.fc1(x))
    x = net.fc2(x)
    output = net.sigmoid(x)
    output = torch.flatten(output)
    prediction = torch.where(output<0.5,0,1).item()
    label = classes[prediction]

    # get the gradient of the output
    output.backward()

    # pool the gradients across the channels
    pooled_grad = torch.mean(feature_grad, dim=[0, 2, 3])

    # weight the channels with the corresponding gradients
    # (L_Grad-CAM = alpha * A)
    features = features.detach()
    for i in range(features.shape[1]):
        features[:, i, :, :] *= pooled_grad[i] 

    # average the channels and create an heatmap
    # ReLU(L_Grad-CAM)
    heatmap = torch.mean(features, dim=1).squeeze()
    heatmap = np.maximum(heatmap, 0)

    # normalization for plotting
    heatmap = heatmap / torch.max(heatmap)
    heatmap = heatmap.numpy()

    # project heatmap onto the input image
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * 0.4 + img
    superimposed_img = np.uint8(255 * superimposed_img / np.max(superimposed_img))
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)

    Image.fromarray(superimposed_img).save("./static/img/grad-cam_img.png")

    return output,label
    
if __name__ == "__main__":
    paths_gen = glob.glob("data/test_data_2/generated_data/*png")
    paths_real = glob.glob("data/test_data_2/real_data/*jpg")

    paths = paths_gen + paths_real

    for p in paths:
        output,img = output_result(p, gradcam_flag=True)
        basename = os.path.basename(p).split(".")[0]
        name = "inf_" + basename +"_"+ str(output.item()).split(".")[1][:4] + ".png"
        img = Image.fromarray(img)
        img.save("./out/tmp3/"+name)
