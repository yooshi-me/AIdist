import pandas as pd
from PIL import Image
import numpy as np
from tqdm import tqdm

#----------------------------------------------
#生成画像の中から、真っ黒の画像を検索するプログラム
#真っ黒画像を抜いたpathの一覧をcsvファイルとして出力する
#-----------------------------------------------


paths_list_path = "./data/pahts_list.csv"
out_path = "./data/pahts_list_without_black_img.csv"


paths_list_df = pd.read_csv(paths_list_path)

black_img_sample_path = "data/face/genarated_data/woman_00211.png" # 真っ黒画像の一例
black_img_sample = np.array(Image.open(black_img_sample_path))

black_img_list = []

paths_list = paths_list_df["path"].to_list()

for p in tqdm(paths_list):
    img = np.array(Image.open(p))
    if np.array_equal(img,black_img_sample):
        black_img_list.append(p)

new_paths_list_df = paths_list_df[~paths_list_df["path"].isin(black_img_list)]

print(black_img_list)
new_paths_list_df.to_csv(out_path, index = False)
