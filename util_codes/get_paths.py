import os
import glob
import torch
import torchvision
import csv

generated_datapath = "data/face/genarated_data/*.png"
real_datapath =  "data/face/real_data/*.jpg"
out_path = "./data/pahts_list.csv"

genarated_files = glob.glob(generated_datapath)
real_files = glob.glob(real_datapath)

all_paths = [["path","generated_flag"]]
#labels = {"airplane":0,"automobile":0,"bird":0,"cat":0,"deer":0,"dog":0,"frog":0,"horse":0,"ship":0,"truck":0}

for file in genarated_files:
    all_paths.append([file,1])


for file in real_files[:len(genarated_files)]:
    all_paths.append([file,0])

f = open(out_path,"w", newline="")
writer = csv.writer(f)

writer.writerows(all_paths)