
import numpy as np
#import pandas as pd
import cv2
import matplotlib.pyplot as plt
import os
 
from PIL import Image
#from glob import glob
import glob
import xml.etree.ElementTree as ET 
import torch
import torchvision
from torchvision import transforms
import datetime
import yaml

from .test_dataloader import test_dataloader


def test(image_path):
    data=[image_path]
    
        
    
    dataloder=test_dataloader(data,1)

    model=torch.load("./mask_dec/FRCNN.pt")

    dataset_class = ['mask', 'no-mask']

    data_class=dataset_class
    data_class.insert(0, "__background__")
    classes = tuple(data_class)
    colors = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(100,100,100),(50,50,50),(255,255,0),(255,0,255),(0,255,255),(100,100,0),(0,100,100))
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')    
    model.to(device)

    model.eval()



    

    #bbox表示の閾値
    s=0.7

    ALL_box=0
    font = cv2.FONT_HERSHEY_SIMPLEX

    for images,image_ids in dataloder:
        images = list(image.to(device) for image in images)
        with torch.no_grad():
            prediction = model(images)
        

        for j in range(len(images)):
            
            imgfile=image_path+'/'+image_ids[j]+'.jpg'
            img = cv2.imread(imgfile)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            num_boxs=0

            for i,box in enumerate(prediction[j]['boxes']):
                

                score = prediction[j]['scores'][i].cpu().numpy()
                if score > s:
                    score = round(float(score),2)
                    cat = prediction[j]['labels'][i].cpu().numpy()
                    txt = '{} {}'.format(classes[int(cat)], str(score))
                    
                    cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]
                    c = colors[int(cat)]
                    box=box.cpu().numpy().astype('int')
                    cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), c , 2)
                    cv2.rectangle(img,(box[0], box[1] - cat_size[1] - 2),(box[0] + cat_size[0], box[1] - 2), c, -1)
                    cv2.putText(img, txt, (box[0], box[1] - 2), font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
                    num_boxs+=1
                    ALL_box+=1

            #plt.figure(figsize=(15,10))
            #plt.imshow(img)
            #plt.show()
            #exit()
            t=f'train_model:FRCNN num_box:{num_boxs}'
            cat_size = cv2.getTextSize(t, font, 0.5, 2)[0]
            cv2.rectangle(img,(15, 15 - cat_size[1] - 2),(15+ cat_size[0], 15 +2), (255,255,255), -1)
            cv2.putText(img,t,(15,15),font, 0.5, (0, 0,0), thickness=1, lineType=cv2.LINE_AA)
            if not os.path.exists(f'./mask_dec/output/{datetime.date.today()}'):  # ディレクトリが存在しない場合、作成する。
                os.makedirs(f'./mask_dec/output/{datetime.date.today()}')
            #BGR RGB変換して保存
            cv2.imwrite(f"./mask_dec/output/{datetime.date.today()}/{image_ids[j]}.jpg",cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    return num_boxs

    

def test2(image_path):


    model=torch.load("./mask_dec/FRCNN.pt")

    dataset_class = ['mask', 'no-mask']

    data_class=dataset_class
    data_class.insert(0, "__background__")
    classes = tuple(data_class)
    colors = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(100,100,100),(50,50,50),(255,255,0),(255,0,255),(0,255,255),(100,100,0),(0,100,100))
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')    
    model.to(device)

    model.eval()
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_tensor = torchvision.transforms.functional.to_tensor(img)

    with torch.no_grad():
        prediction = model([image_tensor.to(device)])
    
    num_boxs=0
    for i,box in enumerate(prediction[0]['boxes']):
        score = prediction[0]['scores'][i].cpu().numpy()
        if score > 0.7:#0.9
            
            score = round(float(score),2)
            cat = prediction[0]['labels'][i].cpu().numpy()
            txt = '{} {}'.format(classes[int(cat)], str(score))
            font = cv2.FONT_HERSHEY_SIMPLEX
            cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]
            c = colors[int(cat)]
            box=box.cpu().numpy().astype('int')
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), c , 2)
            cv2.rectangle(img,(box[0], box[1] - cat_size[1] - 2),(box[0] + cat_size[0], box[1] - 2), c, -1)
            cv2.putText(img, txt, (box[0], box[1] - 2), font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
            
            num_boxs+=1
        
    
    t=f'train_model:FRCNN num_box:{num_boxs}'
    cat_size = cv2.getTextSize(t, font, 0.5, 2)[0]
    cv2.rectangle(img,(15, 15 - cat_size[1] - 2),(15+ cat_size[0], 15 +2), (255,255,255), -1)
    cv2.putText(img,t,(15,15),font, 0.5, (0, 0,0), thickness=1, lineType=cv2.LINE_AA)
    if not os.path.exists(f'./mask_dec/output/{datetime.date.today()}'):  # ディレクトリが存在しない場合、作成する。
        os.makedirs(f'./mask_dec/output/{datetime.date.today()}')
    #BGR RGB変換して保存
    
    img_name=image_path.split("/")[-1]
    print(f"./mask_dec/output/{datetime.date.today()}/{img_name}")
    cv2.imwrite(f"./mask_dec/output/{datetime.date.today()}/{img_name}",cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    return num_boxs


