# coding:utf-8
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split 
import tensorflow as tf
import os
import sys
import pickle 
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation,Flatten,Multiply
from sklearn.preprocessing import OneHotEncoder
from keras.layers import Input, Dense, merge
from keras.models import Model
from keras.models import load_model
from keras import optimizers

class attention:
	def show_accuracy(self,x_train,y_hat,y_train,name):
		"""
		calculate the training results
		:param x_train: feature matrix of training set 
		:param y_hat: detection result of training set 
		:param y_train: label of training set 
		:param name: apk name
		:return: Accurary 
		"""	

		print(name)
		tp = 0				  
		fp = 0
		tn = 0
		fn = 0
		num = len(x_train)			 
		for i in range(num):		 
			if y_hat[i] == y_train[i]: 
				if y_hat[i] == 0:
					tp += 1
				else:
					tn += 1
			else:
				if y_hat[i] == 0:
					fp += 1
				else:
					fn += 1
		Recall = tp / float(tp + fn)
		Precision = tp / float(tp + fp)
		Accurary = (tp + tn)/float(tp + tn + fn + fp)
		FalseRate = 1 - Precision
		AllFalseRate = 1- Accurary
		print("Total num:",num)
		printlist = ['Precision','Recall','Accurary','FalseRate','AllFalseRate']
		datalist = [Precision,Recall,Accurary,FalseRate,AllFalseRate]
		print(printlist)
		print(datalist)
		frame = pd.DataFrame(datalist,index=printlist)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'trainResult.csv',mode = 'a')
		return Accurary


	def Att(self,att_dim,inputs,name):
		""" attention layer """	
		V = inputs
		QK = Dense(att_dim,bias=None)(inputs)
		QK = Activation("softmax",name=name)(QK)
		MV = Multiply()([V, QK])
		return(MV)

	def train(self,Matrix,label,modelPath):
		""" start train model """		
		dimemsion = 158
		enc = OneHotEncoder()
		label=label.reshape(-1, 1)
		label=enc.fit_transform(label).toarray()
		# print(label)

		X_train,X_test,y_train,y_test=train_test_split(Matrix,label,random_state=1,train_size=0.7)

		inputs = Input(shape=(dimemsion,))
		attention = self.Att(dimemsion,inputs,"attention")
		output = Dense(2, activation='softmax')(attention)
		model = Model(input=[inputs], output=output)
		# sgd = optimizers.SGD(lr=0.001, momentum=0.0, decay=0.0, nesterov=False)
		# adagrad = optimizers.Adagrad(lr=0.001, epsilon=None, decay=0.0)
		# adadelta = optimizers.Adadelta(lr=0.001, rho=0.95, epsilon=None, decay=0.0)
		adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
		model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
		model.fit([X_train], y_train, epochs=20, batch_size=100, shuffle=True, validation_split=0.1)
		
		y_hat_proba = model.predict(X_train)
		y_hat = [round(i[1]) for i in y_hat_proba]
		self.show_accuracy(X_train,y_hat,y_train[:,1],"train set")
		y_hat_proba = model.predict(X_test)
		y_hat = [round(i[1]) for i in y_hat_proba]
		self.show_accuracy(X_test,y_hat,y_test[:,1],"test set")
		
		model.save(modelPath)
		return model

if __name__=='__main__':
	adapter = RF()
	adapter.train(sys.argv[1],sys.argv[2])

