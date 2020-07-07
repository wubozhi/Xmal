# -*- coding: utf-8 -*-
import logging

def Log(self):
	"""log"""
	logPath="log.txt"
	logger = logging.getLogger("RESULT")
	logger.setLevel(logging.INFO)
	if not logger.handlers:
		formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
		file_handler = logging.FileHandler(logPath)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
	return logger
						
