Add new feature extraction methods£¬you can do it by several step like below:
1. Add new feature extraction methods. You should define how to get the feature from one single file in a file like GetAPI.py.
2. Register your new feature extraction methods in FeatureExtraction.py. You should first create your new feature extraction class in line 36 below Method "getFeatures", then add the new method of your new class in line 46, like "GetAPIClass.getAPICalls(Apkpath,bapk,Datapath)"
3. You should also give the code how to deal with the exceptions like line 51,52,53.  
4.That's all