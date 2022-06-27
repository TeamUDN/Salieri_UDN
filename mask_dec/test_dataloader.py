'''
さらに高速化
背景のみの時の改善
スケール、バッジサイズを引数指定可能

'''
import numpy as np 
from PIL import Image
from glob import glob
import xml.etree.ElementTree as ET 
import cv2
 
import torch
import torchvision
from torchvision import transforms
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.utils.data import TensorDataset
import os
import time



class MyDataset(torch.utils.data.Dataset):
        def __init__(self,image_dir,scale):
            
            super().__init__()
            self.image_dir = image_dir
            self.image_ids = sorted(glob('{}/*'.format(image_dir)))
            self.scale=scale
            
        def __getitem__(self, index):
    
            transform = transforms.Compose([
                                            transforms.ToTensor()
            ])
            # 入力画像の読み込み
            
            image_id=self.image_ids[index].split("\\")[-1].split(".jpg")[0]
            image = Image.open(self.image_ids[index])
            image = transform(image)
        
            return image,image_id
        
        def __len__(self):
            return len(self.image_ids)
        
def test_dataloader (data,batch_size,scale=720,shuffle=False):
    itr=0
    for d in data:
        image_dir1=d

        dataset = MyDataset(image_dir1,scale)

        #データのロード
        torch.manual_seed(2020)
        
        if itr == 0:
            train=dataset
        else:
            train=torch.utils.data.ConcatDataset([train,dataset])
        itr=itr+1
        

    def collate_fn(batch):
        return tuple(zip(*batch))
    
    
    test_dataloader = torch.utils.data.DataLoader(train, batch_size=batch_size, shuffle=shuffle,collate_fn=collate_fn, pin_memory=True)#3
    

    return test_dataloader

