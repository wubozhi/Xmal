# -*- coding: utf-8 -*-
import sys
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.core.bytecodes.apk import APK
import os
import re
sys.path.append("."+os.sep+'Log')
from log import Log


class GetAPI:
	def __init__(self):
		"""
		init 
		:param file:
		:return: 
		"""
		self.logger=Log(self)
		
	def getAPICalls(self, Path, fileName, dataPath):
		"""
		get the API Calls
		:param Path: the APK folder path
		:param fileNmae: the APK Nmae
		:param dataPath: the folder path where the api files save
		:return: api files
		"""
		filePath = Path + os.sep + fileName
		self.logger.info("Extract" + fileName + "API calls")
		print("Extract" + fileName + "API calls")
		app = APK(filePath)
		app_dex = dvm.DalvikVMFormat(app.get_dex())
		app_x = analysis.Analysis(app_dex)
		APIs = list()

		classes = [cc.get_name() for cc in app_dex.get_classes()]
		for method in app_dex.get_methods():
			methodBlock = app_x.get_method(method)
			if method.get_code() == None:
				continue
			for i in methodBlock.get_basic_blocks().get():
				for ins in i.get_instructions():
					output = ins.get_output()
					match = re.search(r'(L[^;]*;)->([^\(]*)', output)
					if match and match.group(1) not in classes:
						# print "API: "+match.group()+"	 "+match.group(1)
						if match.group(2) == "<init>":
							continue
						api = match.group()
						if api in APIs:
							continue
						else:
							APIs.append(api)
							
		name = fileName.replace(".apk", "")
		with open(dataPath+os.sep+name+"_API.txt",'w') as f:
			print("Saving " + fileName + " APIs")
			self.logger.info("Saving " + fileName + " APIs")
			for i in range(APIs.__len__()):
					f.write(APIs[i]+"\n")
		
if __name__=='__main__':
	adapter = GetAPI()
	adapter.getAPICalls(sys.argv[1],sys.argv[2],sys.argv[3])

