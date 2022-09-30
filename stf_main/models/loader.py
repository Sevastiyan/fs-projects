import random
import math
import numpy as np
import tensorflow as tf


class loader(tf.keras.utils.Sequence):
    def __init__(self, data, labels, batch_size=64, train=True):
        self.batch_size = batch_size
        self.train = train
        self.length = data.shape[0]
        # print('data', (data == None).any())
        self.data = data
        self.labels = labels
        self.indexes = np.arange(self.length)
        
        if self.train:
            self.on_epoch_end()


    def __len__(self):
        return self.length//self.batch_size


    def __getitem__(self, idx):
        indexes = self.indexes[idx*self.batch_size:(idx+1)*self.batch_size]

        x_batch_list = []
        y_batch_list = []
        for i in indexes:
            y = self.labels[i]            
            y_batch_list.append(y)
            x = self.data[i]

            if self.train: 
                rand = random.random()
                # filter_rand = random.random()

                if rand < 0.33: 
                    x = self.dampen(x, alpha=random.uniform(0, 0.1))
                elif rand < 0.66 and rand >= 0.33:
                    x = self.sharpen(x, alpha=random.uniform(0, 0.1))

                # if filter_rand > 0.50:
                #     # x = lowpass(np.reshape(x, [x, 750]), cutoff=10, fs=50, order=3)
                #     # x = np.reshape(x, [len(x), 750, 1])
                #     x = lowpass(x, cutoff=10, fs=50, order=3)
                #     x = rolling_mean(x, 9)

            x_batch_list.append(x)
        
        x_batch = np.stack(x_batch_list, axis=0)
        y_batch = np.stack(y_batch_list, axis=0)

        return x_batch, y_batch


    def on_epoch_end(self):
        self.indexes = np.arange(self.length)
        if self.train:
            np.random.shuffle(self.indexes)


    def sharpen(self, x, alpha=0.01):
        sec_deriv = self.backward_deriv(x)
        x = (x + sec_deriv * alpha)
        return x


    def dampen(self, x, alpha=0.01):
        sec_deriv = self.backward_deriv(x)
        x = (x - sec_deriv * alpha)
        return x


    def backward_deriv(self, x, step=1):
        left_1 = np.roll(x, shift=-1*step, axis=0)
        left_1[-1*step:] = np.zeros_like(left_1[-1*step:])
        left_2 = np.roll(x, shift=-2*step, axis=0)
        left_2[-2*step:] = np.zeros_like(left_1[-2*step:])

        return x - 2*left_1 + left_2


# def center_deriv(x, step=1):
#    right_roll = np.roll(x, shift=(step+1), axis=0)
#    right_roll[:step+1] = np.zeros_like(right_roll[:step+1])
#    left_roll = np.roll(x, shift=-1*(step+1), axis=0)
#    left_roll[-1*(step):] = np.zeros_like(left_roll[-1*(step):])
   
#    return right_roll - 2*x + left_roll


    # def mask_data(self, data):
    #     # for each mask select a starting index and mask length, then mask data
    #     for _ in range(self.num_masks):
    #         start = randint(0, data.shape[0])
    #         mask_length = randint(self.min_mask_len, self.max_mask_len)
    #         # for each window randomly mask out parts of features
    #         for w in range(data.shape[1]):
    #             if self.random_feature:
    #                 data[start:start+mask_length, w, randint(0, 2)] = 0.0
    #             else:
    #                 data[start:start+mask_length, w, 0] = 0.0
    #                 data[start:start+mask_length, w, 1] = 0.0
    #                 data[start:start+mask_length, w, 2] = 0.0
    #     return data
