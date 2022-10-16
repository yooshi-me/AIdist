import os
import glob
import torch
import torchvision
import csv

generated_datapath = "./data/generated_data/*/*.png"
cifar10_datapath =  "./data/cifar-10/*/*/*.png"
out_path = "./data/pahts_list.csv"

genarated_files = glob.glob(generated_datapath)
cifar10_files = glob.glob(cifar10_datapath)

all_paths = [["path","category","generated_flag"]]
labels = {"airplane":0,"automobile":0,"bird":0,"cat":0,"deer":0,"dog":0,"frog":0,"horse":0,"ship":0,"truck":0}

for file in genarated_files:
    all_paths.append([file,file.split("\\")[-2],0])


for file in cifar10_files:

    label = file.split("\\")[-2]
    if labels[label] >= 2000:
        continue
    labels[label] += 1
    all_paths.append([file,label,1])

f = open(out_path,"w", newline="")
writer = csv.writer(f)

writer.writerows(all_paths)