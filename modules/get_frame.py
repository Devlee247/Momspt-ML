# -*- coding: utf-8 -*-

import os
import torch
from torch.utils.data.dataloader import DataLoader
from lib.dataset.gesture_dataset import GestureDataset
from lib.models import GIFV

def get_frame(csv_path, pretrained_path):
    # ====== CUDA 혹은 CUDNN 설정, GPU 관련 ====== #
    

    # ====== 데이터 로드 ====== #
    dataset = GestureDataset(csvpath=csv_path, mode='prediction')
    data_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=False)

    # ====== 네트워크 가중치 로드 ====== #
    model = GIFV()

    if pretrained_path != '' and os.path.isfile(pretrained_path):
        checkpoint = torch.load(pretrained_path)
        best_performance = checkpoint['loss']
        model.load_state_dict(checkpoint['gen_state_dict'])
        print(f'==> Loaded pretrained model from {pretrained_path}...')
        print(f'Performance test set {best_performance}')
    else:
        print(f'{pretrained_path} is not a pretrained model!!!!')
    
    model.eval()

    front = []
    l_side = []
    r_side = []
    back = []

    for idx, samples in enumerate(data_loader):
        x_test = samples
        prediction = model(x_test)
        pred = prediction.data.max(1,keepdim=True)[1]

        if pred == 0:
            back.append(idx)
        elif pred == 1:
            front.append(idx)
        elif pred == 2:
            l_side.append(idx)
        else:
            r_side.append(idx)

    back_num = int(sum(back)/len(back))

    # Filtering each pose's frames
    l_side = [i for i in l_side if i > back_num]
    r_side = [i for i in r_side if i < back_num]
    back = [i for i in back if i > r_side[-1]]
    front = [i for i in front if i < back_num]

    # Get each pose's frame number
    front_frame_num = int(sum(front)/len(front))
    r_side_frame_num = int(sum(r_side)/len(r_side))
    back_frame_num = int(sum(back)/len(back))
    l_side_frame_num = int(sum(l_side)/len(l_side))
    
    frame_num = {
        'front' : front_frame_num,
        'r_side' : r_side_frame_num,
        'back' : back_frame_num,
        'l_side' : l_side_frame_num
    }

    return frame_num