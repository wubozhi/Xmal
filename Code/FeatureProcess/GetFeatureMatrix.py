# coding:utf-8
import numpy as np
import os
import logging
import sys
sys.path.append("."+os.sep+'GetFeature')
from GetFeature import GetFeature
sys.path.append("."+os.sep+'Log')
from log import Log
import pandas as pd
import threading
import random

class GetFeatureMatrix:
	def __init__(self):
		"""init params"""
		self.featureList = GetFeature().getFeatureList()
		self.APKlist = list()
		self.Matrix = np.zeros((0, self.featureList.__len__()), dtype=int)
		self.label = list()
		self.MatrixLock = threading.Lock()
		self.APKlistLock = threading.Lock()
		self.logger = Log(self)
		
	def featureFromFile(self,filePath):
		"""
		get features from file
		:param filePath: the feature files path
		:return: feature list
		"""
		if not os.path.exists(filePath):
			self.logger.error(filePath+" does not exist")
			print(filePath+" does not exist")
			return
		ls=list()
		with open(filePath,'r',encoding='UTF-8')as f:
			while(True):
				line=f.readline()
				if not line:break
				s=line.replace("\n","")
				s=s.replace("\r","")
				ls.append(s)
		return ls

	def filesInFolder(self, folderPath, suffix):
		"""
		get the files in folderPath
		:param folderPath: the folder path
		:param suffix: the file extension
		:return: files list
		"""
		self.logger.info("Traversing " + folderPath + " folder")
		if not os.path.exists(folderPath):
			self.logger.error(folderPath + " does not exist")
			return
		files = os.listdir(folderPath)
		#print files
		suit = list()
		for file in files:
			if file.endswith(suffix):
				suit.append(file)
		return suit
		
	def getFeaturefromAPK(self,dataPath,apkName):
		"""
		get the features of apkName from feature file in dataPath
		:param dataPath: the folder path where feature files save
		:param apkName: apk name
		:return: feature matrix of apk
		"""
		apiFile = apkName.replace(".apk","_API.txt")
		permissionFile = apkName.replace(".apk","_Permission.txt")
		
		apkFeature = np.zeros((1,self.featureList.__len__()), dtype=int)
		try:		
			perList = self.featureFromFile(dataPath+os.sep+apiFile)
			self.logger.info("Extract "+ apiFile +" feature Matrix")
			print("Extract "+ apiFile +"feature Matrix")
			for p in perList:
				if p in self.featureList:
					i = self.featureList.index(p)
					apkFeature[0][i] = 1
		
			perList = self.featureFromFile(dataPath+os.sep+permissionFile)
			self.logger.info("Extract "+ permissionFile +"feature Matrix")
			print("Extract "+ permissionFile +"feature Matrix")
			for p in perList:
				if p in self.featureList:
					i = self.featureList.index(p)
					apkFeature[0][i] = 1

		except Exception as e:
			self.logger.info(apkName+"feature matrix extraction errors.")
			print(apkName+"feature matrix extraction errors.")
		return apkFeature

	def getFeaturefromDocument(self,dataPath,flag):
		"""
		get the features matrix from dataPath
		:param dataPath: the folder path where feature files save
		:param flag: benign or malicious
		:return: 
		"""
		apks = self.filesInFolder(dataPath, "_Permission.txt")
		for i in range(apks.__len__()):
			apks[i] = apks[i].replace("_Permission.txt",".apk")

		ll = list(set(apks).difference(set(self.APKlist)))
		random.shuffle(ll)
		
		for apk in ll:
			self.APKlistLock.acquire()
			if apk not in self.APKlist:
				self.APKlist.append(apk)
				self.APKlistLock.release()
				features = self.getFeaturefromAPK(dataPath,apk)
				self.MatrixLock.acquire()
				self.Matrix = np.vstack((self.Matrix,features))
				self.label.append(flag)
				self.MatrixLock.release()
			else:
				self.APKlistLock.release()


	def getFeatureMatric(self,benDatapath,malDatapath):
		"""
		get the features matrix from benDatapath and malDatapath
		:param dataPath: the folder path where feature files save
		:param benDatapath: the folder where the feature files of benign APKs save
		:param malDatapath: the folder where the feature files of malicious APKs save
		:return: 
		"""

		print("Start multithreading to extract API features")
		bthreads = []
		mthreads = []
		
		for i in range(10):
			bthread= threading.Thread(target=self.getFeaturefromDocument, args=(benDatapath,0) )
			bthreads.append(bthread)
		
		for i in range(10):
			mthread= threading.Thread(target=self.getFeaturefromDocument, args=(malDatapath,1) )
			mthreads.append(mthread)
			
		for bthread in bthreads:
			bthread.start()
		for mthread in mthreads:
			mthread.start()
		
		for bthread in bthreads:
			bthread.join()
		for mthread in mthreads:
			mthread.join()
		print("exist multithreading")
		
		self.label = np.array(self.label)
		return self.Matrix,self.label,self.featureList
		

if __name__=='__main__':
	adapter = GetFeatureMatrix()
	Matrix,label,EachfeaNum,featureList = adapter.getFeatureMatric(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	print(Matrix)
	print(label)
	print(EachfeaNum)
	print(featureList)

