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
from tfidf import TfIdf
from util import file_exists
from util import exit_error
from util import setup_logger
from util import verify_stemmer
from util import get_values
from util import valida_termo
from engine import Engine
from vector_space_model import VectorSpaceModel
from xml.etree.ElementTree import ElementTree
from nltk.stem.porter import PorterStemmer
from math import log

stemmer = None

def modelo(filename):
	logger = setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND % filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	afile = open(filename, 'rb')
	struct = pickle.load(afile)
	afile.close()
	
	logger.debug(util.STRUCTURE_LOADED % filename)
	
	return struct
	
def consultas(filename, struct):
	logger = setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READING_QUERIES % filename)
	
	query_list = {}
	query_results = {}
	
	with open(filename) as fp:
		count = 0
		for line in fp:
			key, query = trata_query(line)
			query_list[key] = query
			count = count + 1
			
	logger.debug(util.LINES_READED_FILE % (count, filename))
	
	start_time = time.time()
	
	engine = Engine(TfIdf(), struct)
	query_results = engine.search(query_list)
	
	logger.debug(util.QUERIES_TIME % (time.time() - start_time))
	
	return query_results
	
def resultados(filename, query_results):
	logger = setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_RESULTS % filename)
	
	fw = open(filename, 'w') 
	
	for key in query_results:
		fw.write(str(key) + ';' + str(query_results[key]) + '\n')
		
	fw.close()
	
def trata_query(line):

	line = line[:-1]
	vet_line = line.split(util.CSV_SEPARATOR)
	
	identifier = vet_line[0]
	query = vet_line[1]
	
	query = query.replace('/', ' ')
	query = re.sub(' +',' ',query)
	words_array = nltk.word_tokenize(query)
	
	for word in words_array:
		if valida_termo(word) == None:
			words_array.remove(word)
	
	if stemmer:
		words_array = [stemmer.stem(word).upper() for word in words_array]
	
	return (identifier, words_array)
	
def parse_command_file():
	logger =  setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	query_results = {}
	
	model = False
	query = False
	results = False
	config_file = util.SEARCHER_FILENAME
	
	struct = None
	
	if not file_exists(config_file):
		logger.error(util.FILE_NOT_FOUND % config_file)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % config_file)
	
	with open(config_file) as fp:
		count = 0
		for line in fp:
			if count == 0:
				global stemmer
				stemmer = verify_stemmer(line, count, util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
				count = count + 1
				continue
			
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
			
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
	logger.debug(util.CONFIG_END_PROCESSING % config_file)

if __name__ == "__main__":
	parse_command_file()
