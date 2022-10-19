import os
import glob
import torch
import torchvision
import csv

generated_datapath = ""
real_datapath =  "./data/search_images/cat/*.jpg"
out_path = "./data/pahts_list_inference.csv"

genarated_files = glob.glob(generated_datapath)
real_files = glob.glob(real_datapath)

all_paths = [["path","category","generated_flag"]]

for file in genarated_files:
    all_paths.append([file,file.split("\\")[-2],0])


for file in real_files:
    all_paths.append([file,file.split("\\")[-2],1])

f = open(out_path,"w", newline="")
writer = csv.writer(f)

writer.writerows(all_paths)