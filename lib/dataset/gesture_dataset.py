import torch
import pandas as pd
from torch.utils.data import Dataset

class GestureDataset(Dataset):
    def __init__(self, csvpath, mode = 'train'):
        self.mode = mode

        df = pd.read_csv(csvpath)
        if self.mode == 'train':
            df = df.dropna()
            self.input = df.iloc[:,2:].values
            self.output = df.iloc[:,1].values.reshape(len(df.iloc[:,1].values),1)
        else:
            self.input = df.iloc[:,2:].values

    def __len__(self):
        return len(self.input)

    def __getitem__(self, idx):
        if self.mode == 'train':
            input  = torch.FloatTensor(self.input[idx])
            output  = torch.LongTensor(self.output[idx])
            
            return input, output
        else:
            input = torch.FloatTensor(self.input[idx])

            return input