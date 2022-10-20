import glob
from PIL import Image
from tqdm import tqdm

paths = glob.glob("data/face/genarated_data/*.png")


for p in tqdm(paths):
    im = Image.open(p)
    if im.size != (178,178):
        print(p)