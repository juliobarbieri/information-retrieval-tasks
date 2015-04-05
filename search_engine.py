#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 1 2015
@author: Julio Barbieri
"""

import numpy as np
import nltk
import logging
import pickle
import time
import re
import util
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from inverted_list import InvertedList
from metric import Metric
from vector_space_model import VectorSpaceModel
from xml.etree.ElementTree import ElementTree
from nltk.stem.snowball import EnglishStemmer
from math import log

def modelo(filename):
	logger = setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND % fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	afile = open(filename, 'rb')
	struct = pickle.load(afile)
	afile.close()
	
	logger.debug(util.STRUCTURE_LOADED % filename)
	
	return struct
	
def consultas(filename, struct):
	logger = setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READING_QUERIES % filename)
	
	query_list = {}
	query_results = {}
	
	with open(filename) as fp:
		count = 0
		for line in fp:
			key, query = get_values(line, count, util.CSV_SEPARATOR, util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
			query_list[key] = query
			count = count + 1
			
	logger.debug(util.LINES_READED_FILE % (count, filename))
	
	start_time = time.time()
	
	metric = Metric(struct)
	query_results = metric.search(query_list)
	
	logger.debug(util.QUERIES_TIME % (time.time() - start_time))
	
	return query_results
	
def resultados(filename, query_results):
	logger = setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_RESULTS % filename)
	
	fw = open(filename, 'w') 
	
	for key in query_results:
		fw.write(str(key) + ';' + str(query_results[key]) + '\n')
		
	fw.close()
	
def parse_command_file():
	logger =  setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	query_results = {}
	
	model = False
	query = False
	results = False
	fname = util.SEARCH_ENGINE_FILENAME
	
	struct = None
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND % fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
			
			if next_cmd == util.CMD_MODELO and results == False:
				model = True
				struct = modelo(filename)
			elif next_cmd == util.CMD_CONSULTAS and model == True and results == False:
				query = True
				query_results = consultas(filename, struct)
			elif next_cmd == util.CMD_RESULTADOS and model == True and query == True and results == False:
				results = True
				resultados(filename, query_results)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG % count)
	logger.debug(util.CONFIG_END_PROCESSING % fname)

if __name__ == "__main__":
	parse_command_file()
