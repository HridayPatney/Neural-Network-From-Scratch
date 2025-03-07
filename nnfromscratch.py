# -*- coding: utf-8 -*-
"""NNFromScratch.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GG5QEZoY6lyWPgyI6vEwiPfge5VRrXo9
"""

import numpy as np
import pandas as pd
df=pd.read_csv('train.csv')
df.head()

df=np.array(df)

m,n=df.shape
np.random.shuffle(df)

m

n

df_dev=df[0:1000].T

Y_dev=df_dev[0]
X_dev=df_dev[1:n]
X_dev=X_dev/255

df_train=df[1000:m].T
Y_train=df_train[0]
X_train=df_train[1:n]
X_train=X_train/255
_,m_train = X_train.shape

Y_train

def start():
  W1=np.random.rand(10,784)-0.5
  b1=np.random.rand(10,1)-0.5
  W2=np.random.rand(10,10)-0.5
  b2=np.random.rand(10,1)-0.5
  return W1,b1,W2,b2

def softmax(Z):
  A=np.exp(Z)/sum(np.exp(Z))
  return A

def predict(A2):
  return np.argmax(A2,0)
def accuracy(Y_hat,Y):
  return np.sum(Y_hat==Y)/Y.size

def ForwardPass(W1,b1,W2,b2,X):
  Z1=W1.dot(X)+b1
  A1=np.maximum(Z1,0) # relu func
  Z2=W2.dot(A1)+b2
  A2=softmax(Z2)
  return Z1,A1,Z2,A2

def encode(Y):
  encodedY=np.zeros((Y.size,10))
  encodedY[np.arange(Y.size),Y]=1
  return encodedY.T

def derivativeAct(Z):
  return Z > 0

def backwardPass(Z1,A1,Z2,A2,W1,W2,X,Y):
  one_hotY=encode(Y)
  dZ2=A2-one_hotY
  dW2=1/m * dZ2.dot(A1.T)
  db2=1/m * np.sum(dZ2)

  dZ1=W2.T.dot(dZ2)* derivativeAct(Z1)
  dW1=1/m* dZ1.dot(X.T)
  db1=1/m* np.sum(dZ1)
  return dW1,db1,dW2,db2

def update_params(W1,b1,W2,b2,dW1,db1,dW2,db2,LR):
  W1=W1-LR*dW1
  b1=b1-LR*db1
  W2=W2-LR*dW2
  b2=b2-LR*db2
  return W1,b1,W2,b2

def gradient_descent(X,Y,iterations,LR):
  W1,b1,W2,b2=start()
  for i in range(iterations):
    Z1,A1,Z2,A2=ForwardPass(W1,b1,W2,b2,X)
    dW1,db1,dW2,db2=backwardPass(Z1,A1,Z2,A2,W1,W2,X,Y)
    W1,b1,W2,b2=update_params(W1,b1,W2,b2,dW1,db1,dW2,db2,LR)
    if i%100==0:
      print("Iteration: ",i)
      print("Accuracy: ",accuracy(predict(A2),Y))
  return W1,b1,W2,b2

W1,b1,W2,b2=gradient_descent(X_train,Y_train,1000,0.1)

def make_pred(X, W1, b1, W2, b2):
  _,_,_,A2 =ForwardPass(W1,b1,W2,b2,X)
  predictions=predict(A2)
  return predictions

