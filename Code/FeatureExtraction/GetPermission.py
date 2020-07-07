# -*- coding: utf-8 -*-
import sys
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.core.bytecodes.apk import APK
import os
sys.path.append("."+os.sep+'Log')
from log import Log

class GetPermission:
	def __init__(self):
		"""init params"""
		self.logger=Log(self)
		
	def getPermissions(self, Path, fileName,dataPath):
		"""
		get the API Calls
		:param Path: the APK folder path
		:param fileNmae: the APK Nmae
		:param dataPath: the folder path where the permission files save
		:return: permission files
		"""
		filePath = Path + os.sep + fileName
		self.logger.info("Extract" + fileName + " Permissions")
		print("Extract" + fileName + "Permissions")
		app = APK(filePath)
		permissions = app.get_permissions()
		name = fileName.replace(".apk", "")
		with open(dataPath+os.sep+name+"_Permission.txt",'w') as f:
			self.logger.info("Saving" + fileName + " Permissions")
			print("Saving" + fileName + "Permissions")
			for i in range(permissions.__len__()):
				f.write(permissions[i]+"\n")
				
if __name__=='__main__':
	adapter = GetPermission()
	adapter.getPermissions(sys.argv[1],sys.argv[2],sys.argv[3])

