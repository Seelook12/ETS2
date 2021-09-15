import cv2
import pandas as pd

#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-
# 코드 내부에 한글을 사용가능 하게 해주는 부분입니다.

# 딥러닝을 구동하는 데 필요한 케라스 함수를 불러옵니다.
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
# 필요한 라이브러리를 불러옵니다.
import numpy as np
import tensorflow as tf
import pandas as pd
# 실행할 때마다 같은 결과를 출력하기 위해 설정하는 부분입니다.
np.random.seed(3)
tf.random.set_seed(3)

a = pd.read_csv('./Data/new0825.csv')

a1 = [a.iloc[:]['Smean'],a.iloc[:]['Vmean'],a.iloc[:]['Sstd'],a.iloc[:]['Vstd'],a.iloc[:]['S']]
a1 = np.transpose(a1)
X = a1[:,0:4]
Y = a1[:,4]

Y_train = to_categorical(Y, 24)


model = Sequential()
model.add(Dense(20, input_dim=4, activation='relu'))
model.add(Dense(20,  activation='relu'))
model.add(Dense(20,  activation='relu'))
model.add(Dense(60,  activation='relu'))

model.add(Dense(24, activation='sigmoid'))

weights = model.get_weights()

# 딥러닝을 실행합니다.
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y_train, epochs=100000, batch_size=1000)
model.save('new_model1S.h5')
# print(weights)
