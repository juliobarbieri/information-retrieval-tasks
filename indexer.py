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

def leia(filename):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND % filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	indexes = {}
	
	start_time = time.time()
	
	with open(filename) as fp:
		lidos = 0
		aproveitados = 0
		for line in fp:
			termo, documentos = trata_lista(line)
			lidos = lidos + 1
			if termo != None:
				indexes[termo] = documentos
				aproveitados = aproveitados + 1
				
	logger.debug(util.WORDS_TIME % (time.time() - start_time))
	
	logger.debug(util.LINES_READED_USED_FILE % (lidos, aproveitados, filename))
	
	unique_ids = []
	unique_terms = []
	
	for i in indexes:
		unique_ids.extend(indexes[i])
		unique_terms.append(i)
	
	struct = VectorSpaceModel(list(set(unique_ids)), unique_terms)
	struct.setup_matrix(indexes)
	
	return struct
	
def escreva(filename, struct):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.SAVING_STRUCTURE % filename)
	
	afile = open(filename, 'wb')
	pickle.dump(struct, afile)
	afile.close()
	
def trata_lista(line):
	line = line[:-1]
	vet_line = line.split(util.CSV_SEPARATOR)
	
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
		logger.error(util.FILE_NOT_FOUND % fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
			
			if next_cmd == util.CMD_LEIA and count == 0:
				struct = leia(filename)
			elif next_cmd == util.CMD_ESCREVA and count == 1:
				escreva(filename, struct)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG % count)
	logger.debug(util.CONFIG_END_PROCESSING % fname)

parse_command_file()
