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
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	afile = open(filename, 'rb')
	struct = pickle.load(afile)
	afile.close()
	
	#np.set_printoptions(threshold=np.nan)
	
	#print(struct.termo_documento)
	
	logger.debug(util.STRUCTURE_LOADED + filename)
	
	return struct
	
def consultas(filename, struct):
	logger = setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READING_QUERIES + filename)
	
	query_list = {}
	query_results = {}
	
	with open(filename) as fp:
		count = 0
		for line in fp:
			key, query = get_values(line, count, util.CSV_SEPARATOR, util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
			query_list[key] = query
	'''		
	stopwords = nltk.corpus.stopwords.words('english')
	for key in query_list:
		#print(key)
		query = query_list[key]
		words_array = pre_process(query)
		relevances = []
		for word in words_array:
			if word in stopwords:
				continue
			relevance = calc_relevance(struct, word)
			if len(relevances) == 0:
				relevances = relevance
			else:
				#print(str(len(relevances)) + ' ' + str(len(relevance)))
				for i in range(len(relevance)):
					relevances[i] = relevances[i] + relevance[i]
					
		relevances_documents = {}
		
		for element_key, element in zip(struct.name_rows, relevances):
			if element > 0:
				relevances_documents[element_key] = element
		
		relevances_documents = sorted(relevances_documents.items(), key=lambda x: x[1], reverse=True)
		query_results[key] = relevances_documents
		
	print(query_results)
	'''
	metric = Metric(struct)
	query_results = metric.prepare_data(query_list)
	return query_results
	
def resultados(filename, query_results):
	logger = setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_EXPECTED_RESULTS + filename)
	
	fw = open(filename, 'w') 
	
	for key in query_results:
		fw.write(str(key) + ';' + str(query_results[key]) + '\n')
	
def format_text(text):
	chars_to_remove = ['.', ',', '!', '?', ';', ':', '(', ')', '\n']
	sc = set(chars_to_remove)
	text = ''.join([c for c in text if c not in sc])

	return text.upper()
	
'''
def calc_relevance(struct, word):
	stemmer = EnglishStemmer()
	word = stemmer.stem(word).upper()
	#print(word)
	N = struct.qntd_documentos()
	n = struct.qntd_documentos_dado_termo(word)
	total_oc_termo = struct.ocorrencia_total_termo(word)
	#t = struct.qntd_termos()
	
	if n != None and total_oc_termo != None:
		tf = struct.return_term_column(word)/total_oc_termo
		return tf_idf(tf, max(tf), N, n)
	else:
		return np.zeros(N)
	
def tf_idf(tf, max_tf, total_documentos, n):
	tf_idfs = []
	for i in range(len(tf)):
		tf_idf = term_frquency(tf[i], max_tf) * idf(total_documentos, n)
		tf_idfs.append(tf_idf)
	return tf_idfs
	
def term_frquency(tf, max_tf):
	#return 0.5 + ((0.5 * tf)/max_tf)
	return tf/max_tf
	
def idf(total_documentos, n):
	return log(total_documentos/n)
	
def pre_process(query):
	query = query.replace('/', ' ')
	query = re.sub(' +',' ',query)
	words_array = query.split(' ')
	
	return words_array
'''
def parse_command_file():
	logger =  setup_logger(util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
	
	query_results = {}
	
	model = False
	query = False
	results = False
	fname = util.SEARCH_ENGINE_FILENAME
	
	struct = None
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND + fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED + fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_SE_LOGGER, util.SEARCH_ENGINE_LOG)
			
			#if query == False:
			#	logger.error(util.INSTRUCTION_ORDER_ERROR + str(count + 1))
			#	exit_error(util.EXITED_WITH_ERROR)
			
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
				logger.error(util.NE_INSTRUCTION_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG.replace('x', str(count)))
	logger.debug(util.CONFIG_END_PROCESSING)

parse_command_file()
