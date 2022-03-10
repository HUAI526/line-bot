//
//  ai.py
//  
//
//  Created by Huai on 2022/3/10.
//
from keras.models import load_model
import numpy as np
from keras.preprocessing.image import load_img, img_to_array

class AI(object):
    def __init__(self):
        super(AI, self).__init__()
        
        self.init_default()
        
        
        label = np.array(['not','tissue'])
        # 載入模型
        model = load_model('cnn_tissue.h5')
        # 導入圖片
        # image = load_img('/Users/huai/Desktop/python/ML/train/cats_and_dogs_small/test/cats/cat.1700.jpg')
        input_shape = model.input_shape[1:3]

    def predict(path, thresh=0.6):
        img = load_img(path, target_size=input_shape, interpolation='lanczos')
        img = img_to_array(img) / 255.
        conf = model.predict(img.reshape(-1, *img.shape))[0][0]
        thing = 'not' if conf < thresh else 'tissue'
        return (thing, conf)
