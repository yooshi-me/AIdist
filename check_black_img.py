import pandas as pd
from PIL import Image
import numpy as np
from tqdm import tqdm

#----------------------------------------------
#生成画像の中から、真っ黒の画像を検索するプログラム
#真っ黒画像のpathの一覧をcsvファイルとして出力する
#-----------------------------------------------


paths_list_path = "./data/pahts_list.csv"
out_path = "./data/black_img_pahts_list.csv"


paths_list_df = pd.read_csv(paths_list_path)

black_img_sample_path = "data\generated_data\horse\horse_00173.png" # 真っ黒画像の一例
black_img_sample = np.array(Image.open(black_img_sample_path))

black_img_list = []

for p in tqdm(paths_list_df["path"].to_list()):
    img = np.array(Image.open(p))
    if np.array_equal(img,black_img_sample):
        black_img_list.append(p)

print(black_img_list)
pd.Series(black_img_list).to_csv(out_path)
