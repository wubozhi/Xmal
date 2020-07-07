# coding:utf-8
import os
import sys
from sklearn.externals import joblib
sys.path.append("."+os.sep+'FeatureExtraction')
from FeatureExtraction import FeatureExtraction
sys.path.append('FeatureProcess')
from FeatureProcess import FeatureProcess
sys.path.append("."+os.sep+'ModelTrain')
from attention import attention
sys.path.append("."+os.sep+'ModelCheck')
from Test import test
from keras.models import load_model

if __name__ == '__main__':
	benApkpath = ".."+os.sep+"BenignAPK"
	malApkPath = ".."+os.sep+"MaliciousAPK"
	benDatapath = ".."+os.sep+"Data"+os.sep+"BenData"
	malDatapath = ".."+os.sep+"Data"+os.sep+"MalData"
	FeaturePath = ".."+os.sep+"Data"+os.sep+"Featurelist"
	matrixPath = ".."+os.sep+"Data"+os.sep+"matrix"
	labelPath = ".."+os.sep+"Data"+os.sep+"label"
	modelPath = ".."+os.sep+"Data"+os.sep+"train_model"
	xtrainPath = ".."+os.sep+"Data"+os.sep+"xtrain"

	#### Extract features from apps #######
	FeatureExtraction().productFeature(benApkpath,malApkPath,benDatapath,malDatapath)
	Matrix,label = FeatureProcess().featureDeal(benDatapath,malDatapath,FeaturePath,matrixPath,labelPath)
	# Matrix = joblib.load(matrixPath)
	# label = joblib.load(labelPath)

	#### Model train #########
	clf = attention().train(Matrix,label,modelPath)

	#### Detect samples #######
	clf=load_model(modelPath)
	test(clf).check()


