# coding:utf-8
from sklearn.externals import joblib
import numpy as np
import os
import sys
sys.path.append("."+os.sep+'Log')
from log import Log
import pickle 
import pandas as pd
from GetFeatureMatrix import GetFeatureMatrix

class FeatureProcess:
	def __init__(self):
		"""init params"""
		self.logger=Log(self)
		
	def featureDeal(self,benDatapath,malDatapath,FeaturePath,matrixPath,labelPath):
		"""
		get the feature matrix and label of the training apks
		:param benDatapath: the folder where the feature files of benign APKs save
		:param malDatapath: the folder where the feature files of malicious APKs save
		:param FeaturePath: the feature file path
		:param matrixPath: the path of feature matrix file
		:param labelPath: the path of feature label file
		:return: Matrix,label
		"""
		GetFeatureMatrixClass = GetFeatureMatrix()
		Matrix,label,featureList= GetFeatureMatrixClass.getFeatureMatric(benDatapath,malDatapath)
		
		joblib.dump(featureList,FeaturePath)
		joblib.dump(Matrix,matrixPath)
		joblib.dump(label,labelPath)
		
		
		print("length:%d"%(Matrix.shape[1]))
		frame = pd.DataFrame(Matrix,columns = featureList)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'feature.csv',index=False)
		frame = pd.DataFrame(label)
		frame.to_csv(".."+os.sep+"Data"+os.sep+'label.csv',header=False,index=False)
		
		return Matrix,label

if __name__=='__main__':
	adapter = FeatureProcess()
	Matrix,label = adapter.featureDeal()
	print(Matrix)
	print(label)

