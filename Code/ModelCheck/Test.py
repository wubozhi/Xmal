 # coding:utf-8
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier 
import lime.lime_tabular
import matplotlib.pyplot as plt
from multiprocessing import Process,Manager,Lock
import numpy as np
import os
import logging
import csv
import pickle 
import pandas as pd
import sys
from lxml import etree
import re
import matplotlib.pyplot as plt
import pandas as pd
import heapq
sys.path.append("."+os.sep+'Log')
from log import Log
sys.path.append(".."+os.sep+'FeatureExtraction')
from FeatureExtraction import FeatureExtraction
from GetAPI import GetAPI
sys.path.append(".."+os.sep+'FeatureProcess')
from GetFeatureMatrix import GetFeatureMatrix
sys.path.append("."+os.sep+'ModelCheck')
from attention_utils import get_activations


class test:
	def __init__(self,clf):
		"""init params"""
		self.clf = clf
		self.trainModel=".."+os.sep+"Data"+os.sep+"train_model.m"
		self.xtrain = ".."+os.sep+"Data"+os.sep+"xtrain"
		self.Check=".."+os.sep+"CheckApk"
		self.DataImportant = ".."+os.sep+"TestData"
		self.CheckData=".."+os.sep+"Data"+os.sep+"CheckData"
		self.TestMatrix = ".."+os.sep+"Data"+os.sep+"testMatrix"
		self.Featurelist= joblib.load(".."+os.sep+"Data"+os.sep+"Featurelist")
		self.logger=Log(self)
		self.FeatureExtractionClass = FeatureExtraction()	
	def getCheckApkFeature(self):
		"""
		get feature files from CheckAPK file
		:return: checkApks 
		"""
		checkApks = self.FeatureExtractionClass.filesInFolder(self.Check, ".apk")
		TestFileLock = Lock()
		m = Manager()
		getTestFile = m.list()
		processes = [Process(target=self.FeatureExtractionClass.getFeatures, args=(self.Check,checkApks,self.CheckData,TestFileLock,getTestFile)) for i in range(3)]
		for p in processes:
			p.start()
		for p in processes:
			p.join()  
		return checkApks

	def getFeatureMatric(self,checkApks):
		"""
		get feature files from CheckAPK file
		:param checkApks: the checkApks files path
		:return: Matrix 
		"""		
		Matrix = np.zeros((0, self.Featurelist.__len__()), dtype=int)
		GetFeatureMatrixClass = GetFeatureMatrix()
		for apk in checkApks:
			features = GetFeatureMatrixClass.getFeaturefromAPK(self.CheckData,apk)
			Matrix = np.vstack((Matrix,features))
		return Matrix
			
		
	def check(self):
		"""
		get the detection result of checkApks 

		"""				
		self.getCheckApkFeature()
		APKlist = []
		for i in self.FeatureExtractionClass.filesInFolder(self.CheckData,"_Permission.txt"):
			APKlist.append(i.replace("_Permission.txt",".apk"))

		Matrix = self.getFeatureMatric(APKlist)

		predict_proba_y = self.clf.predict(Matrix)
		predict_y = [round(i[1]) for i in predict_proba_y]
		print(predict_proba_y)
		print(predict_y)
				
		out = open(".."+os.sep+'Data'+os.sep+'checkResult.csv','w', encoding='utf_8')
		out.write('')
		writer = csv.writer(out,lineterminator='\n')
		writer.writerow(['APKname','Category'])
		
		print("\nAPK checking...\n")
		print("--------------------------------result--------------------------------------")
		for i in range(APKlist.__len__()):
			if predict_y[i] == 1:
				print("APK name:	"+APKlist[i]+"	"+"Category:	Malicious APK\n")
				writer.writerow([APKlist[i],'Malicious APK'])
			else:
				print("APK name:	"+APKlist[i]+"	"+"Category:	Benign APK\n")
				writer.writerow([APKlist[i],'Benign APK'])

		frame = pd.DataFrame(Matrix,columns = self.Featurelist)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'testMatrix.csv',index=False)
				
		attention_vector = get_activations(self.clf, Matrix,print_shape_only=True,layer_name='attention')
		print(attention_vector)
		for j in range(APKlist.__len__()):
			print(APKlist[j])
			writer.writerow(["--------"])
			writer.writerow([APKlist[j]])
			max_num_index_list = map(list(attention_vector[0][j]).index, heapq.nlargest(20, list(attention_vector[0][j])))
			max_num_index_list = list(max_num_index_list)
			f = {}
			for i in max_num_index_list:
				dic = {i:list(attention_vector[0][j])[i]}
				f.update(dic)
			for k in sorted(f,key=f.__getitem__,reverse=True):
			# for i in max_num_index_list:
				if Matrix[j][k] ==1:
					print(self.Featurelist[k],' : ',Matrix[j][k],' : ',f[k],' : ',k )
					writer.writerow([self.Featurelist[k],Matrix[j][k],f[k],k ])
		
		# pd.DataFrame(attention_vector[0][0], columns=['attention']).plot(kind='bar',
																	   # title='Attention Mechanism as '
																			 # 'a function of input'
																			 # ' dimensions.')
		# plt.show()


if __name__=='__main__':
	adapter = test()
	adapter.check()	


