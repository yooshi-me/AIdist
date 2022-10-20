import glob
from PIL import Image
import os
from tqdm import tqdm

real_data_dir_path = "./data/face/real_data/*.jpg"
real_data_paths = glob.glob(real_data_dir_path)

out_path = "./data/face/real_data_croped"

for p in tqdm(real_data_paths):
    base_name = os.path.basename(p)
    im = Image.open(p)
    im.crop((0,10,178,188)).save(os.path.join(out_path,base_name))