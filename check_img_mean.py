import glob
import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt

#-------------------------------------
#各データセットの平均画像を作成するプログラム
#-------------------------------------


cifar10_path = "./data/cifar-10/*/*/*.png"
generated_data_path = "./data/generated_data/*/*.png"


cifar10_paths_list = glob.glob(cifar10_path)
generated_data_paths_list = glob.glob(generated_data_path)



def check(paths_list,name):
    base = np.zeros((32,32,3))

    for p in tqdm(paths_list):
        img = Image.open(p).resize((32,32))
        img = np.array(img,dtype=float)
        base += img

    mean_img = (base / len(paths_list)).astype(np.uint8)
    print(mean_img)
    Image.fromarray(mean_img).save(f"./out/{name}.png")

    return mean_img


check(cifar10_paths_list,"cifar10")
check(generated_data_paths_list,"generated")