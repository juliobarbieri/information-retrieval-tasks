#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 2015
@author: Julio Barbieri
"""

import numpy as np
import nltk
import logging
import re
import pickle
import util
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from inverted_list import InvertedList
from vector_space_model import VectorSpaceModel
from xml.etree.ElementTree import ElementTree
from nltk.stem.snowball import EnglishStemmer

def leia(filename, struct):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	indexes = {}
	
	with open(filename) as fp:
		lidos = 0
		aproveitados = 0
		for line in fp:
			termo, documentos = trata_lista(line)
			lidos = lidos + 1
			if termo != None:
				indexes[termo] = documentos
				aproveitados = aproveitados + 1
				
	logger.debug(util.LINES_READED_USED_FILE.replace('x', str(lidos)).replace('y', str(aproveitados)) + filename)
	
	unique_ids = []
	unique_terms = []
	
	for i in indexes:
		unique_ids.extend(indexes[i])
		unique_terms.append(i)
	
	#set_ids = list(set(unique_ids))
	#set_terms = list(set(unique_terms))
	#np.set_printoptions(threshold=np.nan)
	
	struct = VectorSpaceModel(list(set(unique_ids)), unique_terms)
	struct.setup_matrix(indexes)
	
	#termo_documento = np.zeros((len(set_ids), len(set_terms)))
	
	#for j in range(len(unique_terms)):
	#	for doc in indexes[unique_terms[j]]:
	#		idx = set_ids.index(doc)
	#		termo_documento[idx,j] = termo_documento[idx,j] + 1
	
	
	
def escreva(filename, struct):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.SAVING_STRUCTURE + filename)
	
	afile = open(r'test.pkl', 'wb')
	pickle.dump(struct, afile)
	afile.close()
	
def trata_lista(line):
	line = line[:-1]
	vet_line = line.split(util.INVERTED_LIST_SEPARATOR)
	
	termo = vet_line[0]
	documentos = vet_line[1]
	
	documentos = documentos[:-1]
	documentos = documentos[1:]
	
	vet_docs = documentos.split(',')
	vet_docs = list(map(int, vet_docs)) #[int(i) for i in vet_docs]
	
	if (valida_termo(termo)):
		return (termo, vet_docs)
	else:
		return None, None

def valida_termo(termo):
	if len(termo) > 1 and re.match("^[A-Z]*$", termo):
		return termo
	else:
		return None
	
def parse_command_file():
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	struct = None
	
	fname = util.INDEXER_FILENAME
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND + fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED + fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
			
			if next_cmd == util.CMD_LEIA and count == 0:
				leia(filename, struct)
			elif next_cmd == util.CMD_ESCREVA and count == 1:
				escreva(filename, struct)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG.replace('x', str(count)))
	logger.debug(util.CONFIG_END_PROCESSING)

parse_command_file()
